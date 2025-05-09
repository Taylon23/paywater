from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserPerfil
from django.core.exceptions import ValidationError
from datetime import date


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("As senhas não coincidem.")

        username = cleaned_data.get('username')
        email = cleaned_data.get('email')

        if User.objects.filter(username=username).exists():
            self.add_error(
                'username', 'Este nome de usuário já está em uso. Por favor, escolha outro.')

        if User.objects.filter(email=email).exists():
            self.add_error('email', 'Este e-mail já está em uso.')

        return cleaned_data
    
    
class UserPerfilForm(forms.ModelForm):
    class Meta:
        model = UserPerfil
        fields = ['nome_completo', 'data_nascimento', 'cep',
                  'cpf', 'endereco', 'estado', 'cidade', 'foto','referencia']

    nome_completo = forms.CharField(
        label='Nome Completo',
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Digite seu nome completo'})
    )

    data_nascimento = forms.DateField(
        label='Data de Nascimento',
        widget=forms.DateInput(
            attrs={'class': 'form-control', 'type': 'date'}),
        input_formats=['%Y-%m-%d'],  # Garante o formato correto
        required=True  # Para evitar erro se o campo estiver vazio
    )

    cep = forms.CharField(
        label='CEP',
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Digite seu CEP'})
    )
    cpf = forms.CharField(
        label='CPF',
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Digite seu CPF'})
    )

    endereco = forms.CharField(
        label='Endereço',
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Endereço completo'})
    )

    estado = forms.CharField(
        label='Estado',
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'readonly': True})
    )

    cidade = forms.CharField(
        label='Cidade',
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'readonly': True})
    )

    foto = forms.ImageField(
        label='Foto de Perfil',
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'}),
        required=False  # Torna o campo opcional
    )

    def clean_data_nascimento(self):
        data_nascimento = self.cleaned_data.get('data_nascimento')
        if data_nascimento:
            hoje = date.today()
            idade = hoje.year - data_nascimento.year - \
                ((hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day))

            if idade < 18:
                raise ValidationError(
                    'Você deve ter pelo menos 18 anos para se registrar.')
        return data_nascimento