from django.db import models
from django.utils import timezone


class Agent(models.Model):
    # IdAg : Django crÃ©e dÃ©jÃ  un id auto, mais si tu veux garder IdAg du fichier :
    id_ag = models.PositiveIntegerField(unique=True)

    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)

    qualification = models.CharField(max_length=150, blank=True)
    service = models.CharField(max_length=150, blank=True)
    employeur = models.CharField(max_length=150, blank=True)

    # HDSDefautAg "05:00"
    hds_defaut = models.TimeField(null=True, blank=True)

    # HAjoutQuotidienAg (on ne sait pas si c'est temps ou nombre)
    # Si câ€™est aussi une durÃ©e/heure => TimeField. Sinon => Decimal/Integer.
    hajout_quotidien = models.TimeField(null=True, blank=True)

    echeance_permis = models.DateField(null=True, blank=True)
    echeance_fco = models.DateField(null=True, blank=True)

    # SuppAg (suppression / flag ?)
    supp = models.BooleanField(default=False)
    archive = models.BooleanField(default=False)

    arrivee = models.DateField(null=True, blank=True)
    depart = models.DateField(null=True, blank=True)

    tel = models.CharField(max_length=30, blank=True)

    class Meta:
        ordering = ["nom", "prenom"]

    def __str__(self):
        return f"{self.nom} {self.prenom}"


class Flux(models.Model):
    id_flux = models.AutoField(primary_key=True)
    flux = models.CharField(max_length=150)
    flux_long = models.CharField(max_length=255)
    couleur_flux = models.CharField(max_length=50, blank=True)
    archive = models.BooleanField(default=False)

    class Meta:
        ordering = ["flux"]

    def __str__(self):
        return self.flux


class Energie(models.Model):
    energie = models.CharField(max_length=150)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["energie"]

    def __str__(self):
        return self.energie


class PresenceMotif(models.Model):
    pres = models.CharField(max_length=150)
    presence = models.CharField(max_length=150)
    jour_travail = models.FloatField()
    couleur_hex_motif_presence = models.CharField(max_length=7, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["pres", "presence"]

    def __str__(self):
        return self.pres


class Vehicule(models.Model):
    nom_vehicule = models.CharField(max_length=150)
    type = models.CharField(max_length=150)
    archive = models.BooleanField(default=False)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nom_vehicule


class Collecte(models.Model):
    id_collecte = models.BigAutoField(primary_key=True)
    date_collecte = models.DateField(default=timezone.localdate)

    id_agent_1 = models.ForeignKey(
        Agent,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="collectes_agent_1",
    )
    a1_hr_debut = models.TimeField(null=True, blank=True)
    a1_hr_fin = models.TimeField(null=True, blank=True)

    id_agent_2 = models.ForeignKey(
        Agent,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="collectes_agent_2",
    )
    a2_hr_debut = models.TimeField(null=True, blank=True)
    a2_hr_fin = models.TimeField(null=True, blank=True)

    id_agent_3 = models.ForeignKey(
        Agent,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="collectes_agent_3",
    )
    a3_hr_debut = models.TimeField(null=True, blank=True)
    a3_hr_fin = models.TimeField(null=True, blank=True)

    id_vehicule = models.ForeignKey(
        Vehicule,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="collectes",
    )
    km_depart = models.FloatField(null=True, blank=True)
    km_retour = models.FloatField(null=True, blank=True)

    id_flux1 = models.ForeignKey(
        Flux,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="collectes_flux1",
    )
    id_flux2 = models.ForeignKey(
        Flux,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="collectes_flux2",
    )
    id_flux3 = models.ForeignKey(
        Flux,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="collectes_flux3",
    )
    tonnage1 = models.FloatField(null=True, blank=True)
    tonnage2 = models.FloatField(null=True, blank=True)
    tonnage3 = models.FloatField(null=True, blank=True)

    id_energie_1 = models.ForeignKey(
        Energie,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="collectes_energie1",
    )
    id_energie_2 = models.ForeignKey(
        Energie,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="collectes_energie2",
    )
    id_energie_3 = models.ForeignKey(
        Energie,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="collectes_energie3",
    )
    energie_qte_1 = models.FloatField(null=True, blank=True)
    energie_qte_2 = models.FloatField(null=True, blank=True)
    energie_qte_3 = models.FloatField(null=True, blank=True)

    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date_collecte", "-date_creation"]

    def __str__(self):
        return f"Collecte {self.id_collecte}"
