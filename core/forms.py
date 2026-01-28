from django import forms
from .models import Agent, Flux, Energie, Vehicule


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
        fields = ["flux", "flux_long", "archive"]


class EnergieForm(forms.ModelForm):
    class Meta:
        model = Energie
        fields = ["energie"]


class VehiculeForm(forms.ModelForm):
    class Meta:
        model = Vehicule
        fields = ["nom_vehicule", "type", "archive"]
