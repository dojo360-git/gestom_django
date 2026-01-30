from django import forms
from .models import Agent, Flux, Energie, Vehicule, Collecte


class AgentForm(forms.ModelForm):
    class Meta:
        model = Agent
        fields = [
            "id_ag", "nom", "prenom", "qualification", "service", "employeur",
            "hds_defaut", "hajout_quotidien", "echeance_permis", "echeance_fco",
            "supp", "arrivee", "depart", "tel",
        ]
        widgets = {
            "echeance_permis": forms.DateInput(attrs={"type": "date"}),
            "echeance_fco": forms.DateInput(attrs={"type": "date"}),
            "arrivee": forms.DateInput(attrs={"type": "date"}),
            "depart": forms.DateInput(attrs={"type": "date"}),
            "hds_defaut": forms.TimeInput(attrs={"type": "time"}),
            "hajout_quotidien": forms.TimeInput(attrs={"type": "time"}),
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
            "date_collecte": forms.DateInput(attrs={"type": "date"}),
            "a1_hr_debut": forms.TimeInput(attrs={"type": "time"}),
            "a1_hr_fin": forms.TimeInput(attrs={"type": "time"}),
            "a2_hr_debut": forms.TimeInput(attrs={"type": "time"}),
            "a2_hr_fin": forms.TimeInput(attrs={"type": "time"}),
            "a3_hr_debut": forms.TimeInput(attrs={"type": "time"}),
            "a3_hr_fin": forms.TimeInput(attrs={"type": "time"}),
            "km_depart": forms.NumberInput(attrs={"step": "0.01"}),
            "km_retour": forms.NumberInput(attrs={"step": "0.01"}),
            "tonnage1": forms.NumberInput(attrs={"step": "0.01"}),
            "tonnage2": forms.NumberInput(attrs={"step": "0.01"}),
            "tonnage3": forms.NumberInput(attrs={"step": "0.01"}),
            "energie_qte_1": forms.NumberInput(attrs={"step": "0.01"}),
            "energie_qte_2": forms.NumberInput(attrs={"step": "0.01"}),
            "energie_qte_3": forms.NumberInput(attrs={"step": "0.01"}),
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
            self.fields["a1_hr_debut"].initial = "05:00"
            self.fields["a2_hr_debut"].initial = "05:00"
            self.fields["a3_hr_debut"].initial = "05:00"
            self.fields["a1_hr_fin"].initial = "12:00"
            self.fields["a2_hr_fin"].initial = "12:00"
            self.fields["a3_hr_fin"].initial = "12:00"
