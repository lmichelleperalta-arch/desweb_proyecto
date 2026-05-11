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
    path("prediosupdate_catastrodj/",views.PrediosUpdate.as_view(),name="prediosupdate_catastrodj"),
    path("callesinsert_catastrodj/", views.CallesInsert.as_view(),name="callesinsert_catastrodj"),
    path("callesdelete_catastrodj/",views.CallesDelete.as_view(),name="callesdelete_catastrodj"),
    path("callesselectall_catastrodj/",views.CallesSelectAll.as_view(),name="callesselectall_catastrodj"),
    path("callesselectasdicts_catastrodj/<int:id>/",views.CallesSelectAsDicts.as_view(),name="callesselectasdicts_catastrodj"),
    path("callesupdate_catastrodj/",views.CallesUpdate.as_view(),name="callesupdate_catastrodj"),
    path("iglesiasinsert_catastrodj/", views.IglesiasInsert.as_view(),name="iglesiasinsert_catastrodj"),
    path("iglesiasdelete_catastrodj/",views. IglesiasDelete.as_view(),name="iglesiasdelete_catastrodj"),
    path("iglesiasselectall_catastrodj/",views.IglesiasSelectAll.as_view(),name="iglesiasselectall_catastrodj"),
    path("iglesiasselectasdicts_catastrodj/<int:id>/",views.IglesiasSelectAsDicts.as_view(),name="iglesiasselectasdicts_catastrodj"),
    path("iglesiasupdate_catastrodj/",views.IglesiasUpdate.as_view(),name="iglesiasupdate_catastrodj"),
   
]