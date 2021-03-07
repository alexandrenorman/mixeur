# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _

from helpers.helpers import decode_base64_file
from helpers.views import ApiView, ModelView

from listepro.forms import ProfessionalForm
from listepro.models import KeyWord, Professional, Segment, SubMission
from listepro.serializers import ProfessionalSerializer


def send_mail_on_create_or_update(request, instance, professional_data, created):
    context = {
        "user": request.user,
        "instance": instance,
        "created": created,
    }
    subject = _(
        f"{_('Création') if created else _('Modification')} de la fiche {instance.name}"
    )
    message = _(
        """

<p>Bonjour {{user.last_name}},</p>

<p>L'utilisateur {{instance.user.full_name}} a
{% if created %}créé{% else %}modifié{% endif %} sa fiche {{instance.name}}. </p>
<p>
  Pour visualiser la fiche veuillez suivre le lien :
<a href="{{ protocol }}://{{ domain }}/#/listepro/detail-professionnel/{{instance.id}}">{{ protocol }}://{{ domain }}/#/listepro/detail-professionnel/{{instance.id}}</a>


<br>
<br>
<hr />

<p>
  A très bientôt dans votre espace,<br>
  L'équipe {{site_name}}
</p>

    """  # NOQA: E501
    )

    to_qs = instance.user.group.profile.filter(
        user_type__in=("advisor", "superadvisor")
    )
    for to in to_qs:
        to.send_email(subject, message, context)


class ProfessionalView(ModelView, ApiView):
    """
    Professional View
    """

    model = Professional
    form = ProfessionalForm
    serializer = ProfessionalSerializer
    perm_module = "listepro/professional"
    updated_at_attribute_name = "updated_at"

    # Problem with filter for professional results in search
    def filter(self, request, queryset):  # NOQA: A003
        """
        Filter queryset from request argument
        """
        professional_id = request.GET.get("id")
        professional_user = request.GET.get("user")

        if professional_id and professional_id is not None:
            queryset = queryset.filter(id=professional_id)
        if professional_user and professional_user is not None:
            queryset = queryset.filter(user=professional_user)

        queryset = (
            queryset.prefetch_related("primary_key_words")
            .prefetch_related("secondary_key_words")
            .prefetch_related("primary_key_words__category")
            .prefetch_related("secondary_key_words__category")
            .prefetch_related("secondary_key_words__category")
            .prefetch_related("activity_first")
            .prefetch_related("activity_second")
            .prefetch_related("activity_third")
            .prefetch_related("activity_fourth")
            .prefetch_related("sub_missions__mission")
            .prefetch_related("job")
            .prefetch_related("segments")
            .prefetch_related("user__group")
        )

        return queryset.order_by("?")

    def post_save(self, request, instance, professional_data, created):  # NOQA: C901
        """
        Save professional's M2M field
        """

        self._save_m2m_from_double_list_select(
            instance=instance,
            attribute="segments",
            model_queryset=Segment.objects,
            data=professional_data.get("segments", []),
        )
        self._save_m2m_from_double_list_select(
            instance=instance,
            attribute="primary_key_words",
            model_queryset=KeyWord.objects,
            data=professional_data.get("primary_key_words", []),
        )
        self._save_m2m_from_double_list_select(
            instance=instance,
            attribute="secondary_key_words",
            model_queryset=KeyWord.objects,
            data=professional_data.get("secondary_key_words", []),
        )
        self._save_m2m_from_double_list_select(
            instance=instance,
            attribute="sub_missions",
            model_queryset=SubMission.objects,
            data=professional_data.get("sub_missions", []),
        )

        if "logo" in professional_data:
            if professional_data["logo"] is None:
                instance.logo = None
            else:
                try:
                    instance.logo = decode_base64_file(professional_data["logo"])
                except Exception:
                    if professional_data["logo"].startswith("/media/"):
                        instance.logo = professional_data["logo"].replace("/media/", "")
                    else:
                        instance.logo = professional_data["logo"]
            instance.save()

        if "original_logo" in professional_data:
            if professional_data["original_logo"] is None:
                instance.original_logo = None
            else:
                try:
                    instance.original_logo = decode_base64_file(
                        professional_data["original_logo"]
                    )
                except Exception:
                    if professional_data["original_logo"].startswith("/media/"):
                        instance.original_logo = professional_data[
                            "original_logo"
                        ].replace("/media/", "")
                    else:
                        instance.original_logo = professional_data["original_logo"]
            instance.save()

        send_mail_on_create_or_update(request, instance, professional_data, created)
