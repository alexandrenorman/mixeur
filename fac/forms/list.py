# -*- coding: utf-8 -*-
from django import forms

from fac.models import List, Contact, Organization


from django.utils.translation import ugettext_lazy as _


class ListForm(forms.ModelForm):
    class Meta:
        model = List
        fields = ("id", "title", "description", "use_organizations_as_contacts")

    def clean_lists(self):
        lists = self.cleaned_data["lists"]
        try:
            if self.initial["id"] in [x.id for x in lists]:
                raise forms.ValidationError(
                    _("Vous ne pouvez pas inclure la liste elle-même !")
                )
        except KeyError:
            pass

        for x in lists:
            for y in x.get_lists():
                try:
                    if self.initial["id"] == y.pk:
                        raise forms.ValidationError(
                            _(
                                "Vous ne pouvez pas inclure une liste ({0}) qui inclue déjà cette liste ! "
                            ).format(x)
                        )
                except KeyError:
                    pass

        return lists


class ListListFilterForm(forms.ModelForm):
    class Meta:
        model = List
        fields = ("filter",)

    filter = forms.CharField(label=_("Filtrer"), max_length=80, required=True)


class AddContactToListForm(forms.Form):
    contacts = forms.ModelChoiceField(
        queryset=Contact.objects.all().order_by("pk"),
        empty_label=None,
        label=_("Contact"),
        required=True,
    )
    choosen_list = forms.ModelChoiceField(
        queryset=List.objects.all().order_by("pk"),
        empty_label=None,
        label=_("Liste"),
        required=True,
    )


class AddOrganizationToListForm(forms.Form):
    organizations = forms.ModelChoiceField(
        queryset=Organization.objects.all().order_by("pk"),
        empty_label=None,
        label=_("Organisation"),
        required=True,
    )
    choosen_list = forms.ModelChoiceField(
        queryset=List.objects.all().order_by("pk"),
        empty_label=None,
        label=_("Liste"),
        required=True,
    )
