from django.db import models


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


class Vehicule(models.Model):
    nom_vehicule = models.CharField(max_length=150)
    type = models.CharField(max_length=150)
    archive = models.BooleanField(default=False)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nom_vehicule
