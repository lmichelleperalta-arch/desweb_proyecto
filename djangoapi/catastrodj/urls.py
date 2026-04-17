from django.urls import path, include
from . import views
from rest_framework import routers
from . import views

urlpatterns = [
    path("hello_catastrodj/", views.HelloCatastrodj.as_view(),name="hello_catastrodj"),
    path("prediosinsert_catastrodj/", views.PrediosInsert.as_view(),name="prediosinsert_catastrodj"),
    path("prediosdelete_catastrodj/", views.PrediosDelete.as_view(),name="prediosdelete_catastrodj"),
    path("prediosdelete2_catastrodj/<int:id>/",views.PrediosDelete2.as_view(),name="prediosdelete2_catastrodj"),
    path("prediosselectall_catastrodj/",views.PrediosSelectAll.as_view(),name="prediosselectall_catastrodj"),
    path("prediosselectasdicts_catastrodj/<int:id>/",views.PrediosSelectAsDicts.as_view(),name="prediosselectasdicts_catastrodj"),

]