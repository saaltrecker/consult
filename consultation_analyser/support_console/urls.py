from django.urls import path

from . import views

urlpatterns = [
    path("", views.support_home),
    path("sign-out/", views.sign_out),
    path("ml-pipeline-test/", views.ml_pipeline_test),
]
