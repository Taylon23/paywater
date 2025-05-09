from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('pedido/', views.fazer_pedido, name='fazer_pedido'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
]
