from django.urls import path
from . import views
from django.contrib.auth import views as AuthViews

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(template_name='login.html'), name='login'),
    path('register/', views.register, name='register'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('logout/', AuthViews.LogoutView.as_view(), name="logout"),
    path('perfil/', views.perfil, name="perfil"),
    path('perfil/atualizar/', views.completar_perfil, name='completar-perfil'),
    path('alterar-senha/', views.alterar_senha, name='alterar-senha'),
    path('deletar-conta/', views.deletar_conta, name='deletar-conta'),
    path('meus-pedidos/', views.tabela_pedidos_cliente, name='tabela_pedidos_cliente'),
     path('pedido/<int:pedido_id>/', views.detalhes_pedido, name='detalhes_pedido'),
]