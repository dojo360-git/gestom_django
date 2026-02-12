from django.test import TestCase
from django.urls import reverse
from datetime import date

from .models import Flux, Agent, Vehicule


class FluxTests(TestCase):
    def setUp(self):
        self.flux = Flux.objects.create(
            flux="A Flux",
            flux_long="Alpha long",
            archive=False,
        )

    def test_flux_str(self):
        self.assertEqual(str(self.flux), "A Flux")

    def test_flux_ordering(self):
        Flux.objects.create(flux="B Flux", flux_long="Beta long", archive=False)
        Flux.objects.create(flux="AA Flux", flux_long="AA long", archive=False)
        names = list(Flux.objects.values_list("flux", flat=True))
        self.assertEqual(names, sorted(names))

    def test_flux_list_view(self):
        response = self.client.get(reverse("core:flux_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "A Flux")
        self.assertTemplateUsed(response, "core/flux_list.html")

    def test_flux_detail_view(self):
        response = self.client.get(reverse("core:flux_detail", args=[self.flux.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Alpha long")
        self.assertTemplateUsed(response, "core/flux_detail.html")

    def test_flux_create_view(self):
        response = self.client.post(
            reverse("core:flux_create"),
            data={"flux": "C Flux", "flux_long": "Gamma long", "archive": True},
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Flux.objects.filter(flux="C Flux").exists())

    def test_flux_update_view(self):
        response = self.client.post(
            reverse("core:flux_update", args=[self.flux.pk]),
            data={"flux": "A Flux Updated", "flux_long": "Alpha updated", "archive": True},
        )
        self.assertEqual(response.status_code, 302)
        self.flux.refresh_from_db()
        self.assertEqual(self.flux.flux, "A Flux Updated")
        self.assertTrue(self.flux.archive)

    def test_flux_delete_view(self):
        response = self.client.post(reverse("core:flux_delete", args=[self.flux.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Flux.objects.filter(pk=self.flux.pk).exists())


class AgentTests(TestCase):
    def setUp(self):
        self.agent = Agent.objects.create(
            nom="Durand",
            prenom="Alice",
        )

    def test_agent_str(self):
        self.assertEqual(str(self.agent), "Durand Alice")

    def test_agent_ordering(self):
        Agent.objects.create(nom="Martin", prenom="Zoe")
        Agent.objects.create(nom="Martin", prenom="Alice")
        names = list(Agent.objects.values_list("nom", "prenom"))
        self.assertEqual(names, sorted(names))

    def test_agent_list_view(self):
        response = self.client.get(reverse("core:agent_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Durand")
        self.assertTemplateUsed(response, "core/agent_list.html")

    def test_agent_detail_view(self):
        response = self.client.get(reverse("core:agent_detail", args=[self.agent.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Durand")
        self.assertTemplateUsed(response, "core/agent_detail.html")

    def test_agent_create_view(self):
        response = self.client.post(
            reverse("core:agent_create"),
            data={
                "nom": "Bernard",
                "prenom": "Luc",
                "qualification": "",
                "service": "",
                "employeur": "",
                "supp": False,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Agent.objects.filter(nom="Bernard", prenom="Luc").exists())

    def test_agent_update_view(self):
        response = self.client.post(
            reverse("core:agent_update", args=[self.agent.pk]),
            data={
                "nom": "Durand",
                "prenom": "Alice",
                "qualification": "Senior",
                "service": "Ops",
                "employeur": "Dojo",
                "supp": True,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.agent.refresh_from_db()
        self.assertEqual(self.agent.qualification, "Senior")
        self.assertTrue(self.agent.supp)

    def test_agent_update_echeance_permis_fr_date(self):
        response = self.client.post(
            reverse("core:agent_update", args=[self.agent.pk]),
            data={
                "nom": "Durand",
                "prenom": "Alice",
                "qualification": "",
                "service": "",
                "employeur": "",
                "hds_defaut": "",
                "echeance_permis": "14/02/2026",
                "echeance_fco": "",
                "supp": False,
                "archive": False,
                "arrivee": "",
                "depart": "",
                "tel": "",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.agent.refresh_from_db()
        self.assertEqual(self.agent.echeance_permis, date(2026, 2, 14))

    def test_agent_delete_view(self):
        response = self.client.post(reverse("core:agent_delete", args=[self.agent.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Agent.objects.filter(pk=self.agent.pk).exists())


class VehiculeTests(TestCase):
    def setUp(self):
        self.vehicule = Vehicule.objects.create(
            nom_vehicule="Camion 1",
            type="Camion",
            archive=False,
        )

    def test_vehicule_str(self):
        self.assertEqual(str(self.vehicule), "Camion 1")

    def test_vehicule_list_view(self):
        response = self.client.get(reverse("core:vehicule_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Camion 1")
        self.assertTemplateUsed(response, "core/vehicule_list.html")

    def test_vehicule_detail_view(self):
        response = self.client.get(reverse("core:vehicule_detail", args=[self.vehicule.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Camion 1")
        self.assertTemplateUsed(response, "core/vehicule_detail.html")

    def test_vehicule_create_view(self):
        response = self.client.post(
            reverse("core:vehicule_create"),
            data={"nom_vehicule": "Fourgon 2", "type": "Fourgon", "archive": True},
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Vehicule.objects.filter(nom_vehicule="Fourgon 2").exists())

    def test_vehicule_update_view(self):
        response = self.client.post(
            reverse("core:vehicule_update", args=[self.vehicule.pk]),
            data={"nom_vehicule": "Camion X", "type": "Camion", "archive": True},
        )
        self.assertEqual(response.status_code, 302)
        self.vehicule.refresh_from_db()
        self.assertEqual(self.vehicule.nom_vehicule, "Camion X")
        self.assertTrue(self.vehicule.archive)

    def test_vehicule_delete_view(self):
        response = self.client.post(reverse("core:vehicule_delete", args=[self.vehicule.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Vehicule.objects.filter(pk=self.vehicule.pk).exists())
