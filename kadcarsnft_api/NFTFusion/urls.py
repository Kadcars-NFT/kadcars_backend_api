from django.urls import path
from . import views

urlpatterns = [
    path('renderModel/', views.renderModel, name='renderModel'),
    path('testing/', views.testing),
    path('apply_upgrade/', views.apply_upgrade, name='upgradeEndpoint')
]