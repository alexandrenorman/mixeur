# -*- coding: utf-8 -*-
import json
import uuid
from datetime import datetime

from django import forms
from django.core.exceptions import PermissionDenied, ValidationError
from django.db import IntegrityError, transaction
from django.http import JsonResponse
from django.utils.timezone import make_aware
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from rest_framework import status

from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from core.forms import updatedAtForm

from helpers.json import camel_to_snakecase

# TODO get / post / patch objet simple avec méthodes toutes faites + form + serializer + champs


class PaginationForm(forms.Form):
    page = forms.IntegerField()
    per_page = forms.IntegerField()


class SortForm(forms.Form):
    sort_field = forms.CharField()
    sort_type = forms.ChoiceField(choices=(("asc", "asc"), ("desc", "desc")))


class ApiView(View):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        self._set_request_user_from_jwt()
        self._check_permission()
        try:
            return super().dispatch(request, *args, **kwargs)
        except ValueError:
            return JsonResponse(
                {"error": "object not found"}, status=status.HTTP_404_NOT_FOUND
            )

    def _set_request_user_from_jwt(self):
        jwt = JSONWebTokenAuthentication()
        try:
            auth = jwt.authenticate(self.request)
        except Exception:
            return

        if auth is None:
            return

        self.request.user = auth[0]
        return

    def _check_permission(self):
        return


class LoginRequiredApiView(ApiView):
    def _check_permission(self):
        if self.request.user.is_anonymous:
            raise PermissionDenied
        return


class AdministratorRequiredApiView(ApiView):
    def _check_permission(self):
        if self.request.user.is_anonymous or not self.request.user.is_administrator:
            raise PermissionDenied
        return


class AdministratorOrManagerRequiredApiView(ApiView):
    def _check_permission(self):
        if self.request.user.is_anonymous:
            raise PermissionDenied
        if self.request.user.is_administrator or self.request.user.is_manager:
            return

        raise PermissionDenied
        return


class ExpertRequiredApiView(ApiView):
    def _check_permission(self):
        if self.request.user.is_anonymous or not self.request.user.is_expert:
            raise PermissionDenied
        return


class AdvisorRequiredApiView(ApiView):
    def _check_permission(self):
        if self.request.user.is_anonymous or not self.request.user.is_advisor:
            raise PermissionDenied
        return


class ModelView:
    """
    Standard model view with GET, POST, PATCH and DELETE

    initialize :
    - model
    - form
    - serializer
    - perm_module
    - updated_at_attribute_name

    You can subclass :
    - filter(self, request, queryset)
    - get_serializer(self, request, call)
    - get_form(self, request, call, instance_data)
    """

    model = None
    form = None
    serializer = None
    perm_module = None
    # used to surcharge update_at attribute with another attribute (for list update)
    # use case : update of the object depends of other objects
    updated_at_attribute_name = "updated_at"

    def filter(self, request, queryset):  # NOQA: A003
        """
        Filter queryset from request argument
        """
        return queryset

    def get_perm_module(self, request, call):
        """
        Return perm_module
        """
        return self.perm_module

    def get_serializer(self, request, call):
        """
        Return serializer
        """
        return self.serializer

    def get_form(self, request, call, instance_data):
        """
        Return form
        """
        return self.form

    def get(self, request, *args, **kwargs):
        """"""
        if "pk" in kwargs:
            return self.detail(request, *args, **kwargs)

        return self.list(request, *args, **kwargs)

    def store_get(self, request, *args, **kwargs):
        """"""
        if "pk" in kwargs:
            return self.detail(request, *args, **kwargs)

        return self.store_list(request, *args, **kwargs)

    def get_object(self, pk, request):
        """
        returns the detailed object fetched by pk
        """
        return self.model.objects.get(pk=pk)

    def detail(self, request, *args, **kwargs):
        """
        Get model by [pk]
        """
        pk = kwargs["pk"]

        try:
            obj = self.get_object(pk=pk, request=request)
        except self.model.DoesNotExist:
            return JsonResponse(
                {"error": "object not found"}, status=status.HTTP_404_NOT_FOUND
            )

        perm = self.get_perm_module(request, "GET")
        if perm and not request.user.has_perm(f"{perm}.view", obj):
            return JsonResponse(
                {"error": "view not permitted"}, status=status.HTTP_403_FORBIDDEN
            )

        serializer = self.get_serializer(request, "GET")(obj)
        return JsonResponse(serializer.data)

    def list(self, request, *args, **kwargs):  # NOQA: A003
        """
        List model

        Can be filtered by user [?user=pk]
        """
        objects = self.filter(request=request, queryset=self.model.objects.all())
        store_request = False
        if "limit-to-objects-after" in request.headers:
            store_request = True
            data_updated_at = request.headers["limit-to-objects-after"]
            form = updatedAtForm({"updated_at": data_updated_at})
            if form.is_valid():
                updated_at = make_aware(
                    datetime.fromtimestamp(form.cleaned_data["updated_at"]),
                    is_dst=False,
                )
            else:
                updated_at = None

        else:
            updated_at = None

        perm = self.get_perm_module(request, "LIST")
        if perm:
            allowed_objects = [
                x for x in objects if request.user.has_perm(f"{perm}.view", x)
            ]
        else:
            allowed_objects = objects

        if store_request:
            all_pk = [x.pk for x in allowed_objects]
            all_pk.sort()

        if updated_at:
            filtered_allowed_objects = [
                x
                for x in allowed_objects
                if getattr(x, self.updated_at_attribute_name) > updated_at
            ]
        else:
            filtered_allowed_objects = allowed_objects

        serializer = self.get_serializer(request, "LIST")(
            filtered_allowed_objects, many=True
        )

        if store_request:
            last_update = None
            if allowed_objects:
                last_update = max(x.updated_at for x in allowed_objects)

            try:
                timestamp = last_update.timestamp()
            except AttributeError:
                timestamp = 0

            json_return = {
                "last_updated_at": timestamp,
                "collection": serializer.data,
                "all": all_pk,
            }
            return JsonResponse(json_return, safe=False)

        return JsonResponse(serializer.data, safe=False)

    def _is_get_parameter_is_valid(self, request, parameter):
        return parameter in request.GET and request.GET[parameter] not in [
            "",
            "undefined",
            "null",
        ]

    def _is_request_for_sort(self, request):
        return self._is_get_parameter_is_valid(
            request, "sortField"
        ) and self._is_get_parameter_is_valid(request, "sortType")

    def _is_request_for_pagination(self, request):
        return self._is_get_parameter_is_valid(
            request, "page"
        ) and self._is_get_parameter_is_valid(request, "perPage")

    def _sort_objects(self, request, objects):
        if self._is_request_for_sort(request):
            sort_form = SortForm(
                {
                    "sort_field": request.GET["sortField"],
                    "sort_type": request.GET["sortType"],
                }
            )
            if sort_form.is_valid():
                sort_field = camel_to_snakecase(sort_form.cleaned_data["sort_field"])
                sort_type = sort_form.cleaned_data["sort_type"]

                if sort_type == "asc":
                    order = ""
                else:
                    order = "-"

                objects = objects.order_by(f"{order}{sort_field}")
        else:
            objects = objects.order_by("-updated_at")

        return objects

    def _limit_objects_according_to_pagination(self, request, objects):
        if self._is_request_for_pagination(request):
            pagination_form = PaginationForm(
                {
                    "page": request.GET["page"],
                    "per_page": request.GET["perPage"],
                }
            )
            if pagination_form.is_valid():
                page = pagination_form.cleaned_data["page"]
                per_page = pagination_form.cleaned_data["per_page"]

                if page * per_page > objects.count():
                    objects = objects[
                        max(0, min(objects.count() - per_page, (page - 1) * per_page)) :
                    ]
                else:
                    objects = objects[(page - 1) * per_page : page * per_page]

        return objects

    def delete(self, request, *args, **kwargs):
        """
        Delete model by [pk]

        Must have model.change permission
        """
        try:
            key = kwargs["pk"]
        except KeyError:
            return JsonResponse(
                {"Error": "Not Found"}, status=status.HTTP_400_BAD_REQUEST
            )

        pk = key
        try:
            obj = self.model.objects.get(pk=pk)
        except self.model.DoesNotExist:
            return JsonResponse({}, status=status.HTTP_204_NO_CONTENT)

        perm = self.get_perm_module(request, "DELETE")
        if perm:
            if not request.user.has_perm(f"{perm}.delete", obj):
                return JsonResponse(
                    {"error": "delete not permitted"}, status=status.HTTP_403_FORBIDDEN
                )

        with transaction.atomic():
            self.pre_delete(obj)
            obj.delete()
            self.post_delete(obj)

        return JsonResponse({"ok": "Deleted"})

    def patch(self, request, *args, **kwargs):
        """
        Update model by [pk]

        Must have model.change permission
        """
        try:
            key = kwargs["pk"]
        except KeyError:
            return JsonResponse(
                {"Error": "Not Found"}, status=status.HTTP_404_NOT_FOUND
            )

        object_data = json.loads(request.body)

        pk = key
        try:
            obj = self.model.objects.get(pk=pk)
        except Exception:
            return JsonResponse(
                {"Error": "Not Found"}, status=status.HTTP_404_NOT_FOUND
            )

        perm = self.get_perm_module(request, "PATCH")
        if perm:
            if not request.user.has_perm(f"{perm}.change", obj):
                return JsonResponse(
                    {"error": "change not permitted"}, status=status.HTTP_403_FORBIDDEN
                )

        object_data = self.pre_form(request, object_data, False, args, kwargs)

        form = self.get_form(request, "PATCH", object_data)(object_data, instance=obj)
        if form.is_valid():
            message = ""
            try:
                obj = self._save_object_and_call_post_save(
                    request, form, object_data, created=False
                )
            except IntegrityError as e:
                message = e.__str__()
                return JsonResponse(
                    {"__all__": [message]}, status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return JsonResponse(form.errors, status=status.HTTP_400_BAD_REQUEST)

        return self.get(request, pk=obj.pk)

    def post(self, request, *args, **kwargs):
        """
        Create model by [pk]
        """
        object_data = json.loads(request.body)

        object_data = self.pre_form(request, object_data, True, args, kwargs)

        form = self.get_form(request, "POST", object_data)(object_data)
        if form.is_valid():
            virtual_instance = self._virtual_instance_from_data(form.cleaned_data)
            perm = self.get_perm_module(request, "POST")
            if perm:
                if not request.user.has_perm(f"{perm}.create", virtual_instance):
                    return JsonResponse(
                        {"error": "creation not permitted"},
                        status=status.HTTP_403_FORBIDDEN,
                    )

            message = ""
            try:
                obj = self._save_object_and_call_post_save(
                    request, form, object_data, created=True
                )
            except IntegrityError as e:
                message = e.__str__()
                return JsonResponse(
                    {"__all__": [message]}, status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return JsonResponse(form.errors, status=status.HTTP_400_BAD_REQUEST)

        return self.get(request, pk=obj.pk)

    def _save_object_and_call_post_save(self, request, form, object_data, created):
        with transaction.atomic():
            try:
                obj = form.save()
                self.post_save(request, obj, object_data, created)
            except Exception as e:
                message = str(e)
                raise IntegrityError(message)

        return obj

    def _virtual_instance_from_data(self, data):
        """
        Create a fake instance from data in order to be able to check perm
        """
        instance = self.model(**data)
        instance.id = (
            uuid.uuid4().hex
        )  # Django's has_perm need a primary key to be set...
        return instance

    def pre_form(self, request, instance_data, created=False, *args, **kwargs):
        """
        pre_form operation

        can change instance_data before submiting to form

        created: True if object is created, False if updated
        """
        return instance_data

    def post_save(self, request, instance, instance_data, created=False):
        """
        Handle saving of special fields for POST or PATCH methods

        created: True if object is created, False if updated
        """
        return

    def pre_delete(self, instance):
        """
        Pre-delete operations
        """
        return

    def post_delete(self, instance):
        """
        Post-delete operations
        """
        return

    def _save_m2m_from_pk(self, instance, attribute, model_queryset, pks):
        """
        Save Many2Many field from return values from a SelectValue field

        instance: instance to save
        attribute: attribute of instance
        model_queryset: queryset to use
        pks: pks to save

        Warning : if pks is empty, m2m relation is cleared

        Example:
        places : [2, 1]
        """
        instance.__getattribute__(attribute).clear()

        if pks:
            for pk in pks:
                try:
                    obj = model_queryset.get(pk=pk)  # NOQA: F841
                except Exception:
                    raise ValidationError(
                        f"Le {model_queryset.model._meta.verbose_name} n'existe pas"
                    )

            instance.__getattribute__(attribute).add(*pks)

    def _save_m2m_from_select(
        self, instance, attribute, model_queryset, data, track_by="value"
    ):
        """
        Save Many2Many field from return values from a V-Select field

        instance: instance to save
        attribute: attribute of instance
        model_queryset: queryset to use
        data: data to save

        Warning : if data is empty, m2m relation is cleared

        Example:
        places : [
          {
            label: Broteaux
            value: 2
          },
          {
            label: Monchat
            value: 1
          }
        ]
        """
        instance.__getattribute__(attribute).clear()

        if data:
            pks = [x[track_by] for x in data]
            for pk in pks:
                try:
                    obj = model_queryset.get(pk=pk)  # NOQA: F841
                except Exception:
                    raise ValidationError(
                        f"Le {model_queryset.model._meta.verbose_name} n'existe pas"
                    )

            instance.__getattribute__(attribute).add(*pks)

    def _save_m2m_from_double_list_select(
        self, instance, attribute, model_queryset, data
    ):
        """
        Save Many2Many field from return values from a DoubleListSelect field

        instance: instance to save
        attribute: attribute of instance
        model_queryset: queryset to use
        data: data to save

        Warning : if data is empty, m2m relation is cleared

        Example:
        places : [
          {
            name: Broteaux
            pk: 2
          },
          {
            name: Monchat
            pk: 1
          }
        ]
        """
        instance.__getattribute__(attribute).clear()

        if data:
            pks = [x["pk"] for x in data]
            for pk in pks:
                try:
                    obj = model_queryset.get(pk=pk)  # NOQA: F841
                except Exception:
                    raise ValidationError(
                        f"Le {model_queryset.model._meta.verbose_name} n'existe pas"
                    )

            instance.__getattribute__(attribute).add(*pks)


class ModelReadOnlyView(ModelView):
    def delete(self, request, *args, **kwargs):
        raise PermissionDenied("Read only view")

    def patch(self, request, *args, **kwargs):
        raise PermissionDenied("Read only view")

    def post(self, request, *args, **kwargs):
        raise PermissionDenied("Read only view")

    def _save_object_and_call_post_save(self, request, form, object_data, created):
        raise PermissionDenied("Read only view")

    def _virtual_instance_from_data(self, data):
        raise PermissionDenied("Read only view")

    def post_save(self, request, instance, instance_data, created=False):
        raise PermissionDenied("Read only view")

    def pre_delete(self, instance):
        raise PermissionDenied("Read only view")

    def post_delete(self, instance):
        raise PermissionDenied("Read only view")

    def _save_m2m_from_select(self, instance, attribute, model_queryset, data):
        raise PermissionDenied("Read only view")


class PreventListViewMixin:
    def list(self, request, *args, **kwargs):  # NOQA: A003
        raise PermissionDenied("Operation not allowed")


class PreventDeleteViewMixin:
    def delete(self, request, *args, **kwargs):
        raise PermissionDenied("Operation not allowed")

    def pre_delete(self, instance):
        raise PermissionDenied("Operation not allowed")

    def post_delete(self, instance):
        raise PermissionDenied("Operation not allowed")


class PreventPatchViewMixin:
    def patch(self, request, *args, **kwargs):
        raise PermissionDenied("Operation not allowed")

    def _save_object_and_call_post_save(self, request, form, object_data, created):
        raise PermissionDenied("Operation not allowed")

    def _virtual_instance_from_data(self, data):
        raise PermissionDenied("Operation not allowed")

    def post_save(self, request, instance, instance_data, created=False):
        raise PermissionDenied("Operation not allowed")


class PreventPostViewMixin:
    def post(self, request, *args, **kwargs):
        raise PermissionDenied("Operation not allowed")

    def _save_object_and_call_post_save(self, request, form, object_data, created):
        raise PermissionDenied("Operation not allowed")

    def _virtual_instance_from_data(self, data):
        raise PermissionDenied("Operation not allowed")

    def post_save(self, request, instance, instance_data, created=False):
        raise PermissionDenied("Operation not allowed")
