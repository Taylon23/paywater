from django.db import models
from django.contrib.auth.models import User
from . import choice
from decimal import Decimal


class Pedido(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pedidos')
    data_criacao = models.DateTimeField(auto_now_add=True) 
    marca = models.CharField(max_length=20, choices=choice.MARCAS)
    quantidade = models.PositiveIntegerField()
    pagamento = models.CharField(max_length=20, choices=choice.PAGAMENTO)
    tipo_entrega = models.CharField(max_length=20, choices=choice.RETIRADA_ENTREGA)
    valor_total = models.DecimalField(max_digits=6, decimal_places=2, default=Decimal('0.00'))

    def calcular_total(self):
        if self.quantidade >= 5:
            preco_unitario = Decimal('4.00')
        else:
            precos = {
                'psiu': {'retirar': Decimal('6.00'), 'entregar': Decimal('7.00')},
                'estrela': {'retirar': Decimal('5.00'), 'entregar': Decimal('6.00')}
            }
            preco_unitario = precos.get(self.marca, {}).get(self.tipo_entrega, Decimal('10.00'))
        return self.quantidade * preco_unitario

    def save(self, *args, **kwargs):
        self.valor_total = self.calcular_total()
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f'User: {self.usuario} - Marca: {self.marca} - Quantidade: {self.quantidade}'
