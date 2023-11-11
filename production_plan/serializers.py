from rest_framework import serializers


class PowerPlantSerializer(serializers.Serializer):
    name = serializers.CharField()
    type = serializers.CharField()
    efficiency = serializers.FloatField()
    pmin = serializers.FloatField()
    pmax = serializers.FloatField()


class FuelsSerializer(serializers.Serializer):
    gas = serializers.FloatField()
    kerosine = serializers.FloatField()
    co2 = serializers.FloatField()
    wind = serializers.FloatField()

    def to_internal_value(self, data):
        return {
            "gas": data.get("gas(euro/MWh)"),
            "kerosine": data.get("kerosine(euro/MWh)"),
            "co2": data.get("co2(euro/ton)"),
            "wind": data.get("wind(%)"),
        }


class ProductionPlanSerializer(serializers.Serializer):
    load = serializers.FloatField()
    fuels = FuelsSerializer()
    powerplants = PowerPlantSerializer(many=True)
