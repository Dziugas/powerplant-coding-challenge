from django.urls import path

from production_plan.views import ProductionPlanView


urlpatterns = [
    path("productionplan/", ProductionPlanView.as_view(), name="productionplan"),
]
