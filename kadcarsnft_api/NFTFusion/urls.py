from django.urls import path
from . import views

urlpatterns = [
    path('renderModel/', views.renderGltfModel, name='renderModel')
]