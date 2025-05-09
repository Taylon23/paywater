from django.shortcuts import render, redirect
from .forms import PedidoForm
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from usuarios import models as Usermodels
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum, Count
from .models import Pedido
from django.utils import timezone
from django.contrib.auth.models import User


def home(request):
    return render(request, 'home.html')


@login_required
def fazer_pedido(request):
    try:
        perfil = Usermodels.UserPerfil.objects.get(usuario=request.user)
    except Usermodels.UserPerfil.DoesNotExist:
        messages.warning(
            request, 'Por favor, complete seu perfil antes de fazer um pedido.')
        return redirect('perfil')

    campos_obrigatorios = [
        perfil.nome_completo,
        perfil.cpf,
        perfil.endereco,
        perfil.cidade,
        perfil.estado,
        perfil.cep,
        # Adicione aqui outros campos obrigatórios do seu model Perfil
    ]

    if not all(campos_obrigatorios):
        messages.warning(
            request, 'Você precisa preencher todos os campos do seu perfil antes de fazer um pedido.')
        # Substitua 'pagina_de_perfil' pela URL da sua página de perfil
        return redirect('perfil')

    if request.method == 'POST':
        form = PedidoForm(request.POST)
        if form.is_valid():
            pedido = form.save(commit=False)
            pedido.usuario = request.user
            pedido.valor_total = pedido.calcular_total()
            pedido.save()

            # Enviar e-mail para o admin
            assunto = f'Novo Pedido de {perfil.nome_completo}'
            mensagem = f"""
Novo pedido realizado!

Cliente: {perfil.nome_completo}
CPF: {perfil.cpf}
E-mail: {request.user.email}

Endereço: {perfil.endereco}, {perfil.cidade} - {perfil.estado}
CEP: {perfil.cep}

Referencia: {perfil.referencia}

Marca: {pedido.marca}
Quantidade: {pedido.quantidade}
Forma de pagamento: {pedido.pagamento}
Entrega: {pedido.tipo_entrega}
Valor Total: R$ {pedido.valor_total:.2f}

Data do Pedido: {pedido.data_criacao.strftime('%d/%m/%Y %H:%M')}
            """

            send_mail(
                assunto,
                mensagem,
                settings.DEFAULT_FROM_EMAIL,
                [settings.EMAIL_ADMIN_RECEIVER],
                fail_silently=False
            )

            messages.success(
                request, 'Pedido realizado com sucesso! Você pode ver seus pedidos abaixo.')
            return redirect('tabela_pedidos_cliente')
    else:
        form = PedidoForm()
    return render(request, 'fazer_pedido.html', {'form': form})


@staff_member_required
def admin_dashboard(request):
    hoje = timezone.now().date()
    primeiro_dia_mes = hoje.replace(day=1)

    total_vendas_hoje = Pedido.objects.filter(data_criacao__date=hoje).count()
    total_vendas_mes = Pedido.objects.filter(
        data_criacao__date__gte=primeiro_dia_mes).count()
    total_vendas_geral = Pedido.objects.count()

    total_dinheiro_hoje = Pedido.objects.filter(data_criacao__date=hoje, pagamento='dinheiro').aggregate(
        Sum('valor_total'))['valor_total__sum'] or 0
    total_dinheiro_mes = Pedido.objects.filter(data_criacao__date__gte=primeiro_dia_mes, pagamento='dinheiro').aggregate(
        Sum('valor_total'))['valor_total__sum'] or 0
    total_dinheiro_geral = Pedido.objects.filter(pagamento='dinheiro').aggregate(
        Sum('valor_total'))['valor_total__sum'] or 0

    usuario_mais_pedidos = User.objects.annotate(
        num_pedidos=Count('pedidos')).order_by('-num_pedidos').first()
    top_usuarios_pedidos = User.objects.annotate(
        num_pedidos=Count('pedidos')).order_by('-num_pedidos')[:5]

    # Total de Psiu
    total_psiu = Pedido.objects.filter(marca__iexact='psiu').aggregate(
        Sum('quantidade'))['quantidade__sum'] or 0

    # Total de Estrela
    total_estrela = Pedido.objects.filter(marca__iexact='estrela').aggregate(
        Sum('quantidade'))['quantidade__sum'] or 0

    # Total de Psiu e Estrela vendidos no mês
    total_agua_mes = Pedido.objects.filter(
        data_criacao__date__gte=primeiro_dia_mes,
        marca__in=['psiu', 'estrela']
    ).aggregate(Sum('quantidade'))['quantidade__sum'] or 0

    context = {
        'total_vendas_hoje': total_vendas_hoje,
        'total_vendas_mes': total_vendas_mes,
        'total_vendas_geral': total_vendas_geral,
        'total_dinheiro_hoje': total_dinheiro_hoje,
        'total_dinheiro_mes': total_dinheiro_mes,
        'total_dinheiro_geral': total_dinheiro_geral,
        'usuario_mais_pedidos': usuario_mais_pedidos,
        'top_usuarios_pedidos': top_usuarios_pedidos,
        'total_agua_mes': total_agua_mes,
        'total_psiu': total_psiu,
        'total_estrela': total_estrela,
    }

    return render(request, 'admin_dashboard.html', context)
