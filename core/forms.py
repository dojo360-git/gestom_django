from django import forms
from .models import Produit

class ProduitForm(forms.ModelForm):
    class Meta:
        model = Produit
        fields = ["nom", "prix", "stock"]



from .models import Agent


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