from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APIClient


class PowerPlantTests(TestCase):
    def setUp(self):
        super(PowerPlantTests, self).setUp()
        self.client = APIClient()

    def test_payloads(self):
        url = reverse("productionplan")
        payload_1 = {
            "load": 480,
            "fuels": {
                "gas(euro/MWh)": 13.4,
                "kerosine(euro/MWh)": 50.8,
                "co2(euro/ton)": 20,
                "wind(%)": 60,
            },
            "powerplants": [
                {
                    "name": "gasfiredbig1",
                    "type": "gasfired",
                    "efficiency": 0.53,
                    "pmin": 100,
                    "pmax": 460,
                },
                {
                    "name": "gasfiredbig2",
                    "type": "gasfired",
                    "efficiency": 0.53,
                    "pmin": 100,
                    "pmax": 460,
                },
                {
                    "name": "gasfiredsomewhatsmaller",
                    "type": "gasfired",
                    "efficiency": 0.37,
                    "pmin": 40,
                    "pmax": 210,
                },
                {
                    "name": "tj1",
                    "type": "turbojet",
                    "efficiency": 0.3,
                    "pmin": 0,
                    "pmax": 16,
                },
                {
                    "name": "windpark1",
                    "type": "windturbine",
                    "efficiency": 1,
                    "pmin": 0,
                    "pmax": 150,
                },
                {
                    "name": "windpark2",
                    "type": "windturbine",
                    "efficiency": 1,
                    "pmin": 0,
                    "pmax": 36,
                },
            ],
        }
        payload_2 = {
            "load": 480,
            "fuels": {
                "gas(euro/MWh)": 13.4,
                "kerosine(euro/MWh)": 50.8,
                "co2(euro/ton)": 20,
                "wind(%)": 0,
            },
            "powerplants": [
                {
                    "name": "gasfiredbig1",
                    "type": "gasfired",
                    "efficiency": 0.53,
                    "pmin": 100,
                    "pmax": 460,
                },
                {
                    "name": "gasfiredbig2",
                    "type": "gasfired",
                    "efficiency": 0.53,
                    "pmin": 100,
                    "pmax": 460,
                },
                {
                    "name": "gasfiredsomewhatsmaller",
                    "type": "gasfired",
                    "efficiency": 0.37,
                    "pmin": 40,
                    "pmax": 210,
                },
                {
                    "name": "tj1",
                    "type": "turbojet",
                    "efficiency": 0.3,
                    "pmin": 0,
                    "pmax": 16,
                },
                {
                    "name": "windpark1",
                    "type": "windturbine",
                    "efficiency": 1,
                    "pmin": 0,
                    "pmax": 150,
                },
                {
                    "name": "windpark2",
                    "type": "windturbine",
                    "efficiency": 1,
                    "pmin": 0,
                    "pmax": 36,
                },
            ],
        }
        payload_3 = {
            "load": 910,
            "fuels": {
                "gas(euro/MWh)": 13.4,
                "kerosine(euro/MWh)": 50.8,
                "co2(euro/ton)": 20,
                "wind(%)": 60,
            },
            "powerplants": [
                {
                    "name": "gasfiredbig1",
                    "type": "gasfired",
                    "efficiency": 0.53,
                    "pmin": 100,
                    "pmax": 460,
                },
                {
                    "name": "gasfiredbig2",
                    "type": "gasfired",
                    "efficiency": 0.53,
                    "pmin": 100,
                    "pmax": 460,
                },
                {
                    "name": "gasfiredsomewhatsmaller",
                    "type": "gasfired",
                    "efficiency": 0.37,
                    "pmin": 40,
                    "pmax": 210,
                },
                {
                    "name": "tj1",
                    "type": "turbojet",
                    "efficiency": 0.3,
                    "pmin": 0,
                    "pmax": 16,
                },
                {
                    "name": "windpark1",
                    "type": "windturbine",
                    "efficiency": 1,
                    "pmin": 0,
                    "pmax": 150,
                },
                {
                    "name": "windpark2",
                    "type": "windturbine",
                    "efficiency": 1,
                    "pmin": 0,
                    "pmax": 36,
                },
            ],
        }
        expected_response_1 = [
            {"name": "windpark1", "p": 90.0},
            {"name": "windpark2", "p": 21.6},
            {"name": "gasfiredbig1", "p": 368.4},
            {"name": "gasfiredbig2", "p": 0.0},
            {"name": "gasfiredsomewhatsmaller", "p": 0.0},
            {"name": "tj1", "p": 0.0},
        ]
        expected_response_2 = [
            {"name": "gasfiredbig1", "p": 380.0},
            {"name": "gasfiredbig2", "p": 100.0},
            {"name": "windpark1", "p": 0.0},
            {"name": "windpark2", "p": 0.0},
            {"name": "gasfiredsomewhatsmaller", "p": 0.0},
            {"name": "tj1", "p": 0.0},
        ]
        expected_response_3 = [
            {"name": "windpark1", "p": 90.0},
            {"name": "windpark2", "p": 21.6},
            {"name": "gasfiredbig1", "p": 460.0},
            {"name": "gasfiredbig2", "p": 338.4},
            {"name": "gasfiredsomewhatsmaller", "p": 0.0},
            {"name": "tj1", "p": 0.0},
        ]
        response = self.client.post(url, payload_1, format="json")
        self.assertEqual(response.data, expected_response_1)

        response = self.client.post(url, payload_2, format="json")
        self.assertEqual(response.data, expected_response_2)

        response = self.client.post(url, payload_3, format="json")
        self.assertEqual(response.data, expected_response_3)
