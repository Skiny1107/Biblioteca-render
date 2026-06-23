from django.urls import path
from . import views

urlpatterns = [
    path('', views.prestamos_home, name='prestamos_home'),
    path('hoy/', views.prestamos_hoy, name='prestamos_hoy'),
]
