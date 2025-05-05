from django.db import models
from django.contrib.auth.models import User
from datetime import date

class UserPerfil(models.Model):
    usuario = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='user_name')
    nome_completo = models.CharField(max_length=220)
    foto = models.ImageField(upload_to='perfil_fotos/', blank=True,
                             null=True, help_text="Foto de perfil do usuário")
    cpf = models.CharField(max_length=14, help_text="CPF do usuário")
    data_nascimento = models.DateField(
        help_text="Data de nascimento do usuário", default=date(2007, 1, 1))
    cep = models.CharField(max_length=9, help_text="CEP do usuário")
    endereco = models.CharField(
        max_length=220, blank=True, null=True, help_text="Endereço completo")
    estado = models.CharField(
        max_length=2, blank=True, null=True, help_text="Estado da instalação (ex: PI)")
    cidade = models.CharField(
        max_length=100, blank=True, null=True, help_text="Cidade do usuário")

    def __str__(self):
        return f"Perfil {self.usuario.username}"
