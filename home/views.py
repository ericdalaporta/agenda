from django.views.generic import TemplateView
from clientes.models import Cliente
from funcionarios.models import Funcionario
from fornecedores.models import Fornecedor
from servicos.models import Servico
from produtos.models import Produto
from agendamentos.models import Agendamento

class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['qtd_clientes'] = Cliente.objects.count()
        context['qtd_funcionarios'] = Funcionario.objects.count()
        context['qtd_fornecedores'] = Fornecedor.objects.count()
        context['qtd_servicos'] = Servico.objects.count()
        context['qtd_produtos'] = Produto.objects.count()
        context['qtd_agendamentos'] = Agendamento.objects.count()
        return context
    