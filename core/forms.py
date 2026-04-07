from django import forms
from django.db.models import Q
from django.utils import timezone
from .models import Agent, Flux, Energie, Vehicule, Collecte, PresenceMotif, Itineraire, HeuresManuelles, Tache


class AgentForm(forms.ModelForm):
    QUALIFICATION_CHOICES = [
        ("", "---------"),
        ("Encadrement", "Encadrement"),
        ("Coordinateur", "Coordinateur"),
        ("Ripeur", "Ripeur"),
        ("Chauffeur", "Chauffeur"),
        ("Suivi du Parc", "Suivi du Parc"),
        ("Laveur PAV", "Laveur PAV"),
        ("Chauffeur-Livreur", "Chauffeur-Livreur"),
        ("Agent PAV", "Agent PAV"),
    ]
    SERVICE_CHOICES = [
        ("", "---------"),
        ("Collecte", "Collecte"),
        ("Précollecte", "Précollecte"),
        ("Propreté", "Propreté"),
    ]
    EMPLOYEUR_CHOICES = [
        ("", "---------"),
        ("Hercule", "Hercule"),
        ("CDEA", "CDEA"),
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        date_formats = ["%Y-%m-%d", "%d/%m/%Y"]
        for field_name in ["echeance_permis", "echeance_fco", "arrivee", "depart"]:
            self.fields[field_name].input_formats = date_formats
            self.fields[field_name].localize = False
            self.fields[field_name].widget.format = "%Y-%m-%d"

        # Force dropdowns instead of datalist-backed text inputs.
        self.fields["qualification"].widget = forms.Select(choices=self.QUALIFICATION_CHOICES)
        self.fields["service"].widget = forms.Select(choices=self.SERVICE_CHOICES)
        self.fields["employeur"].widget = forms.Select(choices=self.EMPLOYEUR_CHOICES)

        # Preserve legacy values if an existing record contains an old label.
        for field_name in ["qualification", "service", "employeur"]:
            current_value = (getattr(self.instance, field_name, "") or "").strip()
            if current_value and current_value not in [value for value, _label in self.fields[field_name].widget.choices]:
                self.fields[field_name].widget.choices = [
                    *self.fields[field_name].widget.choices,
                    (current_value, current_value),
                ]

        if not self.instance.pk:
            self.fields["hds_defaut"].initial = "05:00"
            self.fields["hfs_defaut"].initial = "12:00"
            self.fields["arrivee"].initial = timezone.localdate()
            self.fields["depart"].initial = "2036-12-31"

    class Meta:
        model = Agent
        fields = [
            "nom", "prenom", "service", "qualification", "employeur",
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
        }


class FluxForm(forms.ModelForm):
    class Meta:
        model = Flux
        fields = ["flux", "flux_long", "couleur_flux", "archive"]
        widgets = {
            "couleur_flux": forms.TextInput(
                attrs={
                    "type": "color",
                    "class": "flux-color-input",
                    "aria-label": "Choisir une couleur",
                }
            ),
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


class ItineraireForm(forms.ModelForm):
    class Meta:
        model = Itineraire
        fields = ["itineraire", "regie"]


class VehiculeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        energie_values = list(
            Energie.objects.exclude(energie__isnull=True)
            .exclude(energie__exact="")
            .values_list("energie", flat=True)
            .distinct()
            .order_by("energie")
        )
        choices = [("", "---------")] + [(value, value) for value in energie_values]

        current_value = (self.instance.energie or "").strip()
        if current_value and current_value not in energie_values:
            choices.append((current_value, current_value))

        self.fields["energie"].widget = forms.Select(choices=choices)

    class Meta:
        model = Vehicule
        fields = ["nom_vehicule", "type", "energie", "archive"]


class CollecteForm(forms.ModelForm):
    class Meta:
        model = Collecte
        fields = [
            "date_collecte",
            "id_itineraire",
            "id_agent_1", "a1_hr_debut", "a1_hr_fin",
            "id_agent_2", "a2_hr_debut", "a2_hr_fin",
            "id_agent_3", "a3_hr_debut", "a3_hr_fin",
            "motif_heures_sup", "hr_sup_debut", "hr_sup_fin",
            "id_vehicule", "km_depart", "km_retour", "hr_depot_depart", "hr_depot_retour",
            "id_flux1", "tonnage1",
            "id_flux2", "tonnage2",
            "id_flux3", "tonnage3",
            "energie_qte_1",
            "consignes",
            "info_vehicule",
            "info_collecte",
        ]
        widgets = {
            "date_collecte": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "a1_hr_debut": forms.TimeInput(attrs={"type": "time"}),
            "a1_hr_fin": forms.TimeInput(attrs={"type": "time"}),
            "a2_hr_debut": forms.TimeInput(attrs={"type": "time"}),
            "a2_hr_fin": forms.TimeInput(attrs={"type": "time"}),
            "a3_hr_debut": forms.TimeInput(attrs={"type": "time"}),
            "a3_hr_fin": forms.TimeInput(attrs={"type": "time"}),
            "hr_sup_debut": forms.TimeInput(attrs={"type": "time"}),
            "hr_sup_fin": forms.TimeInput(attrs={"type": "time"}),
            "hr_depot_depart": forms.TimeInput(attrs={"type": "time"}),
            "hr_depot_retour": forms.TimeInput(attrs={"type": "time"}),
            "motif_heures_sup": forms.TextInput(
                attrs={
                    "autocomplete": "off",
                    "list": "motif-heures-sup-options",
                    "placeholder": "ex. : Rattrapages",
                }
            ),
            "km_retour": forms.TextInput(attrs={"inputmode": "numeric", "autocomplete": "off", "placeholder": "60 045"}),
            "tonnage1": forms.TextInput(attrs={"inputmode": "numeric", "autocomplete": "off", "placeholder": "6 400"}),
            "tonnage2": forms.TextInput(attrs={"inputmode": "numeric", "autocomplete": "off", "placeholder": "6 400"}),
            "tonnage3": forms.TextInput(attrs={"inputmode": "numeric", "autocomplete": "off", "placeholder": "6 400"}),
            "energie_qte_1": forms.TextInput(attrs={"inputmode": "numeric", "autocomplete": "off", "placeholder": "45"}),
            "km_depart": forms.TextInput(attrs={"inputmode": "numeric", "autocomplete": "off", "placeholder": "60 000"}),
            "consignes": forms.Textarea(
                attrs={
                    "autocomplete": "off",
                    "placeholder": "Rattrapages et infos : bip, clé école",
                    "rows": 3,
                    "style": "resize: vertical;",
                }
            ),
            "info_vehicule": forms.Textarea(
                attrs={
                    "autocomplete": "off",
                    "placeholder": "incident technique ou panne affectant le véhicule",
                    "rows": 3,
                    "style": "resize: vertical;",
                }
            ),
            "info_collecte": forms.Textarea(
                attrs={
                    "autocomplete": "off",
                    "placeholder": "Rattrapages et infos",
                    "rows": 3,
                    "style": "resize: vertical;",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        agent_qs = Agent.objects.order_by("nom", "prenom")
        self.fields["id_agent_1"].queryset = agent_qs
        self.fields["id_agent_2"].queryset = agent_qs
        self.fields["id_agent_3"].queryset = agent_qs
        self.fields["id_itineraire"].queryset = Itineraire.objects.order_by("regie", "itineraire")
        self.fields["id_vehicule"].queryset = Vehicule.objects.filter(archive=False).order_by("nom_vehicule")
        flux_qs = Flux.objects.filter(archive=False).order_by("flux")
        self.fields["id_flux1"].queryset = flux_qs
        self.fields["id_flux2"].queryset = flux_qs
        self.fields["id_flux3"].queryset = flux_qs
        if not self.instance.pk:
            self.fields["date_collecte"].initial = timezone.localdate()
            self.fields["a1_hr_debut"].initial = "05:00"
            self.fields["a2_hr_debut"].initial = "05:00"
            self.fields["a3_hr_debut"].initial = "05:00"
            self.fields["a1_hr_fin"].initial = "12:00"
            self.fields["a2_hr_fin"].initial = "12:00"
            self.fields["a3_hr_fin"].initial = "12:00"
            self.fields["hr_depot_depart"].initial = "05:00"
            self.fields["hr_depot_retour"].initial = "12:00"

        self.fields["date_collecte"].input_formats = ["%Y-%m-%d"]
        self.fields["date_collecte"].localize = False
        self.fields["date_collecte"].widget.format = "%Y-%m-%d"

    def _clean_integer_numeric_field(self, field_name):
        value = self.cleaned_data.get(field_name)
        if value is None:
            return value
        return float(int(value))

    def clean_km_depart(self):
        return self._clean_integer_numeric_field("km_depart")

    def clean_km_retour(self):
        return self._clean_integer_numeric_field("km_retour")

    def clean_tonnage1(self):
        return self._clean_integer_numeric_field("tonnage1")

    def clean_tonnage2(self):
        return self._clean_integer_numeric_field("tonnage2")

    def clean_tonnage3(self):
        return self._clean_integer_numeric_field("tonnage3")

    def clean_energie_qte_1(self):
        return self._clean_integer_numeric_field("energie_qte_1")


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

        self.fields["presence"].queryset = PresenceMotif.objects.order_by("pres", "presence")

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


class TacheForm(forms.ModelForm):
    class Meta:
        model = Tache
        fields = ["date", "info", "jour_ferie", "etat"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "etat": forms.Select(
                choices=[
                    ("", "---------"),
                    ("ouvert", "ouvert"),
                    ("en_cours", "en cours"),
                    ("cloture", "clôturé"),
                ]
            ),
        }
