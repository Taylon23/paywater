from django import forms
from .models import Pedido


class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['marca', 'quantidade', 'pagamento', 'tipo_entrega']
        widgets = {
            'marca': forms.Select(attrs={'class': 'form-control'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'pagamento': forms.Select(attrs={'class': 'form-control'}),
            'tipo_entrega': forms.Select(attrs={'class': 'form-control'}),
        }
