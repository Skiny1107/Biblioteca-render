from django.urls import path
from . import views

urlpatterns = [
    path('', views.usuarios_home, name='usuarios_home'),
    path('<int:id_usuario>/', views.usuarios_detalle, name='usuarios_detalle'),
]
