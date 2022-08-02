from django.urls import path
from . import views

urlpatterns = [
    path('renderGltfModel/', views.renderGltfModel, name='renderGltfModel')
]