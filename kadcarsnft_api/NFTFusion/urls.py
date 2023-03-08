from django.urls import path
from . import views

urlpatterns = [
    path('apply_upgrade/', views.apply_upgrade, name='upgradeEndpoint')
]