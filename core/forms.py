from django import forms
from django.db.models import Q
from django.utils import timezone
from .models import Agent, Flux, Energie, Vehicule, Collecte, PresenceMotif, HeuresManuelles


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
            self.fields["hfs_defaut"].initial = "12:00"
            self.fields["arrivee"].initial = timezone.localdate()
            self.fields["depart"].initial = "2036-12-31"

    class Meta:
        model = Agent
        fields = [
            "nom", "prenom", "qualification", "service", "employeur",
            "hds_defaut", "hfs_defaut", "echeance_permis", "echeance_fco",
            "arrivee", "depart", "tel",
        ]
        widgets = {
            "echeance_permis": forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
            "echeance_fco": forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
            "arrivee": forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
            "depart": forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
            "hds_defaut": forms.TimeInput(attrs={"type": "time"}),
            "hfs_defaut": forms.TimeInput(attrs={"type": "time"}),
            "qualification": forms.TextInput(attrs={"list": "qualification-options"}),
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


class HeuresManuellesForm(forms.ModelForm):
    class Meta:
        model = HeuresManuelles
        fields = ["date", "agent", "heure_debut", "heure_fin", "presence", "motif_heures_sup"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "heure_debut": forms.TimeInput(attrs={"type": "time"}),
            "heure_fin": forms.TimeInput(attrs={"type": "time"}),
            "motif_heures_sup": forms.TextInput(attrs={"list": "motif-heures-sup-options"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        date_formats = ["%Y-%m-%d", "%d/%m/%Y"]
        self.fields["date"].input_formats = date_formats
        self.fields["date"].localize = False
        self.fields["date"].widget.format = "%Y-%m-%d"

        selected_date = timezone.localdate()
        if self.is_bound:
            date_str = self.data.get("date")
            if date_str:
                for fmt in date_formats:
                    try:
                        selected_date = timezone.datetime.strptime(date_str, fmt).date()
                        break
                    except ValueError:
                        continue
        elif self.instance.pk:
            selected_date = self.instance.date or selected_date
        elif self.initial.get("date"):
            selected_date = self.initial["date"]

        agent_qs = Agent.objects.filter(
            (Q(arrivee__isnull=True) | Q(arrivee__lte=selected_date))
            & (Q(depart__isnull=True) | Q(depart__gte=selected_date))
        ).order_by("nom", "prenom")
        self.fields["agent"].queryset = agent_qs

        pres_values = (
            PresenceMotif.objects.exclude(pres__isnull=True)
            .exclude(pres__exact="")
            .values_list("pres", flat=True)
            .distinct()
            .order_by("pres")
        )
        self.fields["presence"].widget = forms.Select(
            choices=[("", "---------")] + [(v, v) for v in pres_values]
        )

        if not self.instance.pk and not self.is_bound:
            self.fields["date"].initial = selected_date
            first_agent = agent_qs.first()
            if first_agent:
                self.fields["agent"].initial = first_agent.pk
                self.fields["heure_debut"].initial = first_agent.hds_defaut
                self.fields["heure_fin"].initial = first_agent.hfs_defaut

    def clean(self):
        cleaned_data = super().clean()
        agent = cleaned_data.get("agent")
        if agent:
            if not cleaned_data.get("heure_debut"):
                cleaned_data["heure_debut"] = agent.hds_defaut
            if not cleaned_data.get("heure_fin"):
                cleaned_data["heure_fin"] = agent.hfs_defaut
        return cleaned_data
