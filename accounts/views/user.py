# -*- coding: utf-8 -*-
import json

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordContextMixin
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied, ValidationError
from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.http import urlsafe_base64_decode
from django.utils.translation import gettext_lazy as _
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic.edit import UpdateView


from phonenumbers import PhoneNumber

from rest_framework import status

from accounts.forms import (
    AccountForm,
    ChangePasswordForm,
    ResetPasswordForm,
    RgpdConsentForm,
    UserForm,
)
from accounts.models import RgpdConsent, User
from accounts.serializers import (
    UserAndRgpdConsentSerializer,
    UserProfilePicSerializer,
    UserSerializer,
    UserSimpleSerializer,
    UserWithMainHousingSerializer,
)

from core.forms import SearchForm

from helpers.helpers import decode_base64_file
from helpers.views import (
    AdministratorRequiredApiView,
    ApiView,
    ExpertRequiredApiView,
    LoginRequiredApiView,
)

from white_labelling.models import WhiteLabelling


@login_required
def AccountView(request):
    return render(request, "accounts/account.html")


class AccountUpdate(UpdateView):
    model = User
    context_object_name = "User"
    template_name = "accounts/account.html"
    form_class = AccountForm
    success_url = "/"

    def get_object(self, qs=None):
        return self.request.user


class UserAndRgpdConsentCreateOnlyView(ApiView):
    def post(self, request, *args, **kwargs):
        json_data = json.loads(request.body)
        user_data = json_data["user"]
        rgpd_consent_data = json_data["rgpd_consent"]
        domain_name_data = json_data["domain_name"]

        with transaction.atomic():
            user_data["user_type"] = "client"
            form = UserForm(user_data)
            if form.is_valid():
                user = form.save()
            else:
                return JsonResponse(form.errors, status=status.HTTP_400_BAD_REQUEST)

            try:
                white_labelling = WhiteLabelling.objects.get(domain=domain_name_data)
            except:  # NOQA
                pass
            else:
                user.white_labelling = white_labelling
                user.save()

            # Always create new instance
            rgpd_consent_data["user"] = user.pk
            form = RgpdConsentForm(rgpd_consent_data)
            if form.is_valid():
                rgpd_consent = form.save()
            else:
                return JsonResponse(form.errors, status=status.HTTP_400_BAD_REQUEST)

            user.is_active = True
            user.save()

        if "nomail" not in json_data:
            user.send_initialize_account_url()

        instance = {"user": user, "rgpd_consent": rgpd_consent}

        serializer = UserAndRgpdConsentSerializer(instance)
        return JsonResponse(serializer.data)


class UserAndRgpdConsentView(LoginRequiredApiView, UserAndRgpdConsentCreateOnlyView):
    def __get_user_according_to_perm(self, request, pk):
        """
        Get user or raise PermissionDenied if wrong auth
        """
        if request.user.is_anonymous:
            raise PermissionDenied

        user = User.objects.get(pk=pk, is_active=True)

        if not request.user.has_perm("accounts/user.change", user):
            raise PermissionDenied("User")

        return user

    def __get_rgpdconsent_according_to_perm(self, request, pk):
        """
        Get rgpdconsent or raise PermissionDenied if wrong auth
        """
        if request.user.is_anonymous:
            raise PermissionDenied("RgpdConsent")

        rgpdconsents = RgpdConsent.objects.filter(user__is_active=True, user__pk=pk)

        if rgpdconsents.exists():
            rgpdconsent = rgpdconsents.first()
        else:
            rgpdconsent = RgpdConsent.objects.create(user=User.objects.get(pk=pk))

        if not request.user.has_perm("accounts/rgpdconsent.change", rgpdconsent):
            raise PermissionDenied("RgpdConsent")

        return rgpdconsent

    def get(self, request, *args, **kwargs):
        try:
            pk = kwargs["pk"]
        except KeyError:
            user = request.user
            pk = request.user.pk
        else:
            user = get_object_or_404(User, pk=pk)

        user = self.__get_user_according_to_perm(request, pk)
        rgpd_consent = self.__get_rgpdconsent_according_to_perm(request, pk)

        instance = {"user": user, "rgpd_consent": rgpd_consent}

        serializer = UserAndRgpdConsentSerializer(instance)
        return JsonResponse(serializer.data)

    def patch(self, request, *args, **kwargs):
        try:
            key = kwargs["pk"]
        except KeyError:
            return JsonResponse(
                {"Error": "Not Found"}, status=status.HTTP_404_NOT_FOUND
            )

        # TODO : check permissions
        json_data = json.loads(request.body)
        user_data = json_data["user"]
        rgpd_consent_data = json_data["rgpd_consent"]

        pk = key
        user = get_object_or_404(User, pk=pk)

        rgpd_consent_data["user"] = user.pk

        # User group cannot be changed !
        if user.group:
            user_data["group"] = user.group.pk
        else:
            user_data["group"] = None

        if "is_active" not in user_data:
            user_data["is_active"] = user.is_active

        with transaction.atomic():
            form = UserForm(user_data, instance=user)
            if form.is_valid():
                form.save()
            else:
                return JsonResponse(form.errors, status=status.HTTP_400_BAD_REQUEST)

            # Always create new instance
            form = RgpdConsentForm(rgpd_consent_data)
            if form.is_valid():
                form.save()
            else:
                return JsonResponse(form.errors, status=status.HTTP_400_BAD_REQUEST)

        return self.get(request)


class AskForResetPasswordEmailView(ApiView):
    def post(self, request, *args, **kwargs):
        json_data = json.loads(request.body)

        form = ResetPasswordForm(json_data)
        if form.is_valid():
            try:
                user = User.objects.get(email=form.data["email"])
            except ObjectDoesNotExist:
                pass
            else:
                user.send_reset_password_url()

        return JsonResponse({"ok": "done"})


class PasswordChangeView(LoginRequiredApiView):
    def post(self, request, *args, **kwargs):

        data = json.loads(request.body)
        form = ChangePasswordForm(data or None)

        if form.is_valid():
            user = User.objects.get(is_active=True, email=request.user.email)
            old_password = form.cleaned_data["old_password"]
            if not user.check_password(f"{old_password}"):
                return JsonResponse(
                    {"error": True, "msg": "invalid password"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user.set_password(form.cleaned_data["new_password1"])
            user.save()

            return JsonResponse({"ok": True})

        return JsonResponse(
            {"error": True, "msg": form.errors}, status=status.HTTP_400_BAD_REQUEST
        )


class PasswordResetConfirmView(PasswordContextMixin, ApiView):
    form_class = SetPasswordForm
    post_reset_login = False
    post_reset_login_backend = None
    success_url = reverse_lazy("password_reset_complete")
    template_name = "registration/password_reset_confirm.html"
    title = _("Enter new password")
    token_generator = default_token_generator

    @method_decorator(sensitive_post_parameters())
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        assert "uidb64" in kwargs
        assert "token" in kwargs

        self.validlink = False
        self.user = self.get_user(kwargs["uidb64"])

        if self.user is not None:
            token = kwargs["token"]
            if self.token_generator.check_token(self.user, token):
                data = json.loads(self.request.body)
                form = SetPasswordForm(self.user, data)
                if form.is_valid():
                    form.save()

                update_session_auth_hash(self.request, form.user)
                return JsonResponse({"ok": "done"})

        # Display the "Password reset unsuccessful" page.
        return JsonResponse({"error": "not done"}, status=status.HTTP_400_BAD_REQUEST)

    def get_user(self, uidb64):
        try:
            # urlsafe_base64_decode() decodes to bytestring
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User._default_manager.get(pk=uid)
        except (
            TypeError,
            ValueError,
            OverflowError,
            User.DoesNotExist,
            ValidationError,
        ):
            user = None
        return user


class UserView(ExpertRequiredApiView):
    def get(self, request, *args, **kwargs):
        if "pk" in kwargs:
            return self.detail(request, *args, **kwargs)

        return self.list(request, *args, **kwargs)

    def detail(self, request, *args, **kwargs):
        pk = kwargs["pk"]
        user = User.objects.get(pk=pk)
        serializer_to_use = self.choose_serialiser(request)
        serializer = serializer_to_use(user)
        return JsonResponse(serializer.data)

    def choose_serialiser(self, request):
        if "with_housing" in request.GET:
            return UserWithMainHousingSerializer

        return UserSimpleSerializer

    def list(self, request, *args, **kwargs):  # NOQA: A003
        # TODO: ANO use perms to filter !
        if "with_housing" in request.GET and request.GET["with_housing"] == "t":
            users = User.objects.prefetch_related("housing").all()
        else:
            users = User.objects.all()

        if "user_type" in request.GET and request.GET["user_type"] in (
            x[0] for x in User.USER_TYPES
        ):
            users = users.filter(user_type=request.GET["user_type"])

        # Search on group.territories
        # and users without Housing
        if "everywhere" not in request.GET and (
            self.request.user.is_advisor or self.request.user.is_manager
        ):
            territories = self.request.user.group.territories.all()
            users = users.filter(
                Q(housing__inseecode__in=[x.inseecode for x in territories])
                | Q(housing=None)
            )

        if "q" in request.GET:
            query_form = SearchForm(request.GET)
            if not query_form.is_valid():
                return JsonResponse(
                    {"__all__": ["Paramêtre de recherche invalide"]},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            query = query_form.cleaned_data["q"]

            # Hack for searching phone numbers
            if "" == "".join([x for x in query if x not in " +0123456789"]):
                query = "".join([x for x in query if x in "+0123456789"])

            for word in query.split():
                try:
                    phone_number = PhoneNumber(word)  # NOQA: F841
                except ValueError:
                    users = users.filter(
                        Q(last_name__icontains=word)
                        | Q(first_name__icontains=word)
                        | Q(email__icontains=word)
                        | Q(housing__address__icontains=word)
                    )
                else:
                    users = users.filter(phone_cache__icontains=word)

        users = users.distinct()
        serializer_to_use = self.choose_serialiser(request)
        serializer = serializer_to_use(users, many=True)
        return JsonResponse(serializer.data, safe=False)

    def delete(self, request, *args, **kwargs):
        try:
            key = kwargs["pk"]
        except KeyError:
            return JsonResponse(
                {"Error": "Not Found"}, status=status.HTTP_404_NOT_FOUND
            )

        pk = key
        user = get_object_or_404(User, pk=pk)

        if not request.user.has_perm("accounts/user.change", user):
            return JsonResponse(
                {"error": "change not permitted"}, status=status.HTTP_403_FORBIDDEN
            )

        user.delete()

        return JsonResponse({"ok": "Deleted"})

    def patch(self, request, *args, **kwargs):
        try:
            key = kwargs["pk"]
        except KeyError:
            return JsonResponse(
                {"Error": "Not Found"}, status=status.HTTP_404_NOT_FOUND
            )

        user_data = json.loads(request.body)

        pk = key
        user = get_object_or_404(User, pk=pk)

        if not request.user.has_perm("accounts/user.change", user):
            return JsonResponse(
                {"error": "change not permitted"}, status=status.HTTP_403_FORBIDDEN
            )

        if (
            not request.user.has_perm(
                "accounts/user.change_user_type",
                {"user_modified": user, "to_user_type": user_data["user_type"]},
            )
            and user.user_type != user_data["user_type"]
        ):
            return JsonResponse(
                {"error": "change user_type is not permitted"},
                status=status.HTTP_403_FORBIDDEN,
            )

        # User group cannot be changed !
        if "group" in user_data and user.group is not None:
            user_data["group"] = user.group.pk

        form = UserForm(user_data, instance=user)
        if form.is_valid():
            form.save()
        else:
            return JsonResponse(form.errors, status=status.HTTP_400_BAD_REQUEST)

        return self.detail(request, pk=key)

    def post(self, request, *args, **kwargs):
        json_data = json.loads(request.body)

        form = UserForm(json_data)
        if form.is_valid():
            user = form.save()
            if "domain" in json_data:
                if WhiteLabelling.objects.filter(domain=json_data["domain"]).exists():
                    user.white_labelling = WhiteLabelling.objects.get(
                        domain=json_data["domain"]
                    )
                    user.save()
            if "nomail" not in json_data:
                user.send_initialize_account_url()
        else:
            return JsonResponse(form.errors, status=status.HTTP_400_BAD_REQUEST)

        return self.get(request, pk=user.pk)


class UserWithGroupView(AdministratorRequiredApiView):
    def get(self, request, *args, **kwargs):
        users = User.objects.select_related("group").all()
        serializer = UserSerializer(users, many=True)
        return JsonResponse(serializer.data, safe=False)


class UserProfilePicView(LoginRequiredApiView):
    def get(self, request, *args, **kwargs):
        if "pk" in kwargs:
            return self.detail(request, *args, **kwargs)

        return self.list(request, *args, **kwargs)

    def detail(self, request, *args, **kwargs):
        pk = kwargs["pk"]
        user = User.objects.get(pk=pk)
        serializer = UserProfilePicSerializer(user)
        return JsonResponse(serializer.data)

    def patch(self, request, *args, **kwargs):
        try:
            key = kwargs["pk"]
        except KeyError:
            return JsonResponse(
                {"Error": "Not Found"}, status=status.HTTP_404_NOT_FOUND
            )

        user_data = json.loads(request.body)

        pk = key
        user = get_object_or_404(User, pk=pk)

        if not request.user.has_perm("accounts/user.change", user):
            return JsonResponse(
                {"error": "change not permetted"}, status=status.HTTP_403_FORBIDDEN
            )

        user.profile_pic = decode_base64_file(user_data["profile_pic"])
        user.save()

        serializer = UserProfilePicSerializer(user)
        return JsonResponse(serializer.data)
