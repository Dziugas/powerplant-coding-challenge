from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from production_plan.helpers import calculate_production_plan
from production_plan.serializers import ProductionPlanSerializer


class ProductionPlanView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = ProductionPlanSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            production_plan = calculate_production_plan(serializer.data)
            return Response(production_plan)
