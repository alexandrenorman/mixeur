# -*- coding: utf-8 -*-

from django.core.exceptions import ValidationError
from helpers.views import ExpertRequiredApiView, ModelView

from visit_report.models import Report
from visit_report.forms import ReportForm
from visit_report.serializers import ReportSerializer

from visit_report.forms import (
    AppendixForm,
    FaceForm,
    ScenarioForm,
    StepForm,
    SystemForm,
    WorkRecommendationForm,
    FinancialAidForm,
    FinancingForm,
    ScenarioSummaryForm,
)
from visit_report.models import (
    Appendix,
    Face,
    Scenario,
    Step,
    System,
    WorkRecommendation,
    FinancialAid,
    Financing,
    ScenarioSummary,
)


class ReportView(ModelView, ExpertRequiredApiView):
    """
    Report View
    """

    model = Report
    form = ReportForm
    serializer = ReportSerializer
    perm_module = "report"

    def filter(self, request, queryset):
        """
        housing: pk of housing to filter Report
        """
        if "housing" in request.GET:
            queryset = queryset.filter(housing__pk=request.GET["housing"])

        return queryset

    def post_save(self, request, instance, instance_data, created):  # NOQA: C901
        """
        Save all submodels at once
        """
        # import wdb; wdb.set_trace()
        if "appendix_table" in instance_data:
            for data in instance_data["appendix_table"]:
                self._save_sub_form(
                    Appendix, AppendixForm, data, visit_report_instance=instance
                )

        if "faces" in instance_data:
            for data in instance_data["faces"]:
                self._save_sub_form(
                    Face, FaceForm, data, visit_report_instance=instance
                )

        if "steps" in instance_data:
            for data in instance_data["steps"]:
                self._save_sub_form(
                    Step, StepForm, data, visit_report_instance=instance
                )

        if "scenarios" in instance_data:
            for data in instance_data["scenarios"]:
                sub_instance = self._save_sub_form(
                    Scenario, ScenarioForm, data, visit_report_instance=instance
                )

                if "financial_aids" in data:
                    for sub_data in data["financial_aids"]:
                        self._save_sub_form(
                            FinancialAid,
                            FinancialAidForm,
                            sub_data,
                            scenario_instance=sub_instance,
                        )

                if "financings" in data:
                    for sub_data in data["financings"]:
                        self._save_sub_form(
                            Financing,
                            FinancingForm,
                            sub_data,
                            scenario_instance=sub_instance,
                        )

                if "scenario_summaries" in data:
                    for sub_data in data["scenario_summaries"]:
                        self._save_sub_form(
                            ScenarioSummary,
                            ScenarioSummaryForm,
                            sub_data,
                            scenario_instance=sub_instance,
                        )

        if "systems" in instance_data:
            for data in instance_data["systems"]:
                self._save_sub_form(
                    System, SystemForm, data, visit_report_instance=instance
                )

        if "work_recommendations" in instance_data:
            for data in instance_data["work_recommendations"]:
                self._save_sub_form(
                    WorkRecommendation,
                    WorkRecommendationForm,
                    data,
                    visit_report_instance=instance,
                )

        return

    def _save_sub_form(
        self, model, form, form_data, visit_report_instance=None, scenario_instance=None
    ):
        instance = None
        sub_instance = None
        if "pk" in form_data:
            pk = form_data["pk"]
            try:
                instance = model.objects.get(pk=pk)
            except Exception:
                pass

        if visit_report_instance:
            form_data["report"] = visit_report_instance.pk

        if scenario_instance:
            form_data["scenario"] = scenario_instance.pk

        this_form = form(form_data, instance=instance)

        if this_form.is_valid():
            sub_instance = this_form.save()

        else:
            raise ValidationError(
                f"Validation Error for {model.__name__} / {this_form.errors}"
            )

        return sub_instance
