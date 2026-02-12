from django import forms
from django.utils import timezone
from .models import Agent, Flux, Energie, Vehicule, Collecte, PresenceMotif


class AgentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        date_formats = ["%Y-%m-%d", "%d/%m/%Y"]
        for field_name in ["echeance_permis", "echeance_fco", "arrivee", "depart"]:
            self.fields[field_name].input_formats = date_formats
            self.fields[field_name].localize = False
            self.fields[field_name].widget.format = "%Y-%m-%d"
        if not self.instance.pk:
            self.fields["hds_defaut"].initial = "05:00"
            self.fields["arrivee"].initial = timezone.localdate()
            self.fields["depart"].initial = "2036-12-31"

    class Meta:
        model = Agent
        fields = [
            "nom", "prenom", "qualification", "service", "employeur",
            "hds_defaut", "echeance_permis", "echeance_fco",
            "supp", "archive", "arrivee", "depart", "tel",
        ]
        widgets = {
            "echeance_permis": forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
            "echeance_fco": forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
            "arrivee": forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
            "depart": forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
            "hds_defaut": forms.TimeInput(attrs={"type": "time"}),
            "employeur": forms.TextInput(attrs={"list": "employeur-options"}),
            "service": forms.TextInput(attrs={"list": "service-options"}),
        }


class FluxForm(forms.ModelForm):
    class Meta:
        model = Flux
        fields = ["flux", "flux_long", "couleur_flux", "archive"]
        widgets = {
            "couleur_flux": forms.TextInput(attrs={"type": "color"}),
        }


class EnergieForm(forms.ModelForm):
    class Meta:
        model = Energie
        fields = ["energie"]


class PresenceMotifForm(forms.ModelForm):
    class Meta:
        model = PresenceMotif
        fields = [
            "pres",
            "presence",
            "jour_travail",
            "couleur_hex_motif_presence",
        ]
        widgets = {
            "couleur_hex_motif_presence": forms.TextInput(attrs={"type": "color"}),
        }


class VehiculeForm(forms.ModelForm):
    class Meta:
        model = Vehicule
        fields = ["nom_vehicule", "type", "archive"]


class CollecteForm(forms.ModelForm):
    class Meta:
        model = Collecte
        fields = [
            "date_collecte",
            "id_agent_1", "a1_hr_debut", "a1_hr_fin",
            "id_agent_2", "a2_hr_debut", "a2_hr_fin",
            "id_agent_3", "a3_hr_debut", "a3_hr_fin",
            "id_vehicule", "km_depart", "km_retour",
            "id_flux1", "tonnage1",
            "id_flux2", "tonnage2",
            "id_flux3", "tonnage3",
            "id_energie_1", "energie_qte_1",
            "id_energie_2", "energie_qte_2",
            "id_energie_3", "energie_qte_3",
        ]
        widgets = {
            "date_collecte": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "a1_hr_debut": forms.TimeInput(attrs={"type": "time"}),
            "a1_hr_fin": forms.TimeInput(attrs={"type": "time"}),
            "a2_hr_debut": forms.TimeInput(attrs={"type": "time"}),
            "a2_hr_fin": forms.TimeInput(attrs={"type": "time"}),
            "a3_hr_debut": forms.TimeInput(attrs={"type": "time"}),
            "a3_hr_fin": forms.TimeInput(attrs={"type": "time"}),
            "km_depart": forms.TextInput(attrs={"inputmode": "numeric", "autocomplete": "off"}),
            "km_retour": forms.TextInput(attrs={"inputmode": "numeric", "autocomplete": "off"}),
            "tonnage1": forms.TextInput(attrs={"inputmode": "numeric", "autocomplete": "off"}),
            "tonnage2": forms.TextInput(attrs={"inputmode": "numeric", "autocomplete": "off"}),
            "tonnage3": forms.TextInput(attrs={"inputmode": "numeric", "autocomplete": "off"}),
            "energie_qte_1": forms.TextInput(attrs={"inputmode": "numeric", "autocomplete": "off"}),
            "energie_qte_2": forms.TextInput(attrs={"inputmode": "numeric", "autocomplete": "off"}),
            "energie_qte_3": forms.TextInput(attrs={"inputmode": "numeric", "autocomplete": "off"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        agent_qs = Agent.objects.order_by("nom", "prenom")
        self.fields["id_agent_1"].queryset = agent_qs
        self.fields["id_agent_2"].queryset = agent_qs
        self.fields["id_agent_3"].queryset = agent_qs
        self.fields["id_vehicule"].queryset = Vehicule.objects.filter(archive=False).order_by("nom_vehicule")
        flux_qs = Flux.objects.filter(archive=False).order_by("flux")
        self.fields["id_flux1"].queryset = flux_qs
        self.fields["id_flux2"].queryset = flux_qs
        self.fields["id_flux3"].queryset = flux_qs
        energie_qs = Energie.objects.order_by("energie")
        self.fields["id_energie_1"].queryset = energie_qs
        self.fields["id_energie_2"].queryset = energie_qs
        self.fields["id_energie_3"].queryset = energie_qs

        if not self.instance.pk:
            self.fields["date_collecte"].initial = timezone.localdate()
            self.fields["a1_hr_debut"].initial = "05:00"
            self.fields["a2_hr_debut"].initial = "05:00"
            self.fields["a3_hr_debut"].initial = "05:00"
            self.fields["a1_hr_fin"].initial = "12:00"
            self.fields["a2_hr_fin"].initial = "12:00"
            self.fields["a3_hr_fin"].initial = "12:00"

        self.fields["date_collecte"].input_formats = ["%Y-%m-%d"]
        self.fields["date_collecte"].localize = False
        self.fields["date_collecte"].widget.format = "%Y-%m-%d"
