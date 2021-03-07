# -*- coding: utf-8 -*-
from helpers.views import ApiView, ModelView

from listepro.forms import ProfessionalProductionForm
from listepro.models import ProfessionalProduction, UsageIntegrated
from listepro.serializers import ProfessionalProductionSerializer


class ProfessionalProductionView(ModelView, ApiView):
    """
    ProfessionalProduction View
    """

    model = ProfessionalProduction
    form = ProfessionalProductionForm
    serializer = ProfessionalProductionSerializer
    perm_module = "listepro/professionalproduction"
    updated_at_attribute_name = "updated_at"

    def filter(self, request, queryset):  # NOQA: A003
        """
        Filter queryset from request argument
        """
        pro = request.GET.get("professional")
        idProd = request.GET.get("id")

        if pro:
            queryset = queryset.filter(professional=pro)
        if idProd:
            queryset = queryset.filter(id=idProd)

        queryset = (
            queryset.prefetch_related("professional")
            .prefetch_related("calculation_method")
            .prefetch_related("usage_integrated")
        )

        return queryset

    def post_save(self, request, instance, production_data, created):
        """
        Save production's M2M field
        """

        self._save_m2m_from_double_list_select(
            instance=instance,
            attribute="usage_integrated",
            model_queryset=UsageIntegrated.objects,
            data=production_data.get("usage_integrated", []),
        )
