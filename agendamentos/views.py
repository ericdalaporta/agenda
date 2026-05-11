from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.db import transaction
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, \
    DetailView

from produtos.models import Produto
from servicos.models import ProdutosServico
from .forms import AgendamentoListForm, AgendamentoModelForm, \
    AgendamentosServicoInLine
from .models import Agendamento, OrdemServicos


class AgendamentosView(ListView):
    model = Agendamento
    template_name = 'agendamentos.html'

    def get_context_data(self, **kwargs):
        context = super(AgendamentosView, self).get_context_data(**kwargs)
        if self.request.GET:
            form = AgendamentoListForm(self.request.GET)
        else:
            form = AgendamentoListForm()
        context['form'] = form
        return context

    def get_queryset(self):
        qs = Agendamento.objects.all().prefetch_related('ordem_servicos_agendamento__servico')
        if self.request.GET:
            form = AgendamentoListForm(self.request.GET)
            if form.is_valid():
                cliente = form.cleaned_data.get('cliente')
                funcionario = form.cleaned_data.get('funcionario')
                if cliente:
                    qs = qs.filter(cliente=cliente)
                if funcionario:
                    qs = qs.filter(funcionario=funcionario)
        if qs.count()>0:
            paginator = Paginator(qs, 10)
            listagem = paginator.get_page(self.request.GET.get('page'))
            return listagem
        else:
            return messages.info(self.request, 'Não existem agendamentos cadastrados')

class AgendamentoAddView(SuccessMessageMixin, CreateView):
    model = Agendamento
    form_class = AgendamentoModelForm
    template_name = 'agendamento_form.html'
    success_url = reverse_lazy('agendamentos')
    success_message = 'Agendamento criado com sucesso'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['frm_inline'] = AgendamentosServicoInLine(self.request.POST)
        else:
            data['frm_inline'] = AgendamentosServicoInLine()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        frm_inline = context['frm_inline']
        with transaction.atomic():
            if frm_inline.is_valid():
                self.object = form.save()
                frm_inline.instance = self.object
                frm_inline.save()
                return super().form_valid(form)
            else:
                return self.render_to_response(self.get_context_data(form=form))



class AgendamentoUpdateView(SuccessMessageMixin, UpdateView):
    model = Agendamento
    form_class = AgendamentoModelForm
    template_name = 'agendamento_form.html'
    success_url = reverse_lazy('agendamentos')
    success_message = 'Agendamento atualizado com sucesso'

    def get_queryset(self):
        return super().get_queryset().prefetch_related('ordem_servicos_agendamento')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['frm_inline'] = AgendamentosServicoInLine(self.request.POST, instance=self.object)
        else:
            data['frm_inline'] = AgendamentosServicoInLine(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        frm_inline = context['frm_inline']
        if frm_inline.is_valid():
            for form_item in frm_inline:
                if not form_item.cleaned_data or form_item.cleaned_data.get('DELETE'):
                    continue
                situacao = form_item.cleaned_data.get('situacao')
                servico = form_item.cleaned_data.get('servico')
                if situacao != 'C':
                    produtoservico = ProdutosServico.objects.filter(servico=servico)
                    if produtoservico:
                        for prd in produtoservico:
                            produto = prd.produto
                            if produto.quantidade < prd.quantidade:
                                messages.error(self.request, f'Atenção! Quantidade em estoque insuficiente para o produto {produto.nome}')
                                return self.render_to_response(self.get_context_data(form=form))
        with transaction.atomic():
            if frm_inline.is_valid():
                self.object = form.save()
                frm_inline.instance = self.object
                frm_inline.save()
                return super().form_valid(form)
            else:
                return self.render_to_response(self.get_context_data(form=form))

class AgendamentoDeleteView(SuccessMessageMixin, DeleteView):
    model = Agendamento
    template_name = 'agendamento_apagar.html'
    success_url = reverse_lazy('agendamentos')
    success_message = 'Agendamento apagado com sucesso'

class AgendamentoExibir(DetailView):
    model = Agendamento
    template_name = 'agendamento_exibir.html'

    def get_object(self, queryset=None):

        agendamento = Agendamento.objects.get(pk=self.kwargs.get('pk'))
        if agendamento.status == 'A':
            ordem_servico = OrdemServicos.objects.filter(agendamento=agendamento)
            lista_situacao = ordem_servico.values_list('situacao', flat=True)
            if 'A' in lista_situacao:
                messages.info(self.request, 'Ordem de serviço não pode ser encerrada. Existem serviços com a situação em aberto!')
            else:
                for ordem in ordem_servico:
                    if ordem.situacao == 'R':
                        if ordem.servico.produto:
                            produto_servico = ProdutosServico.objects.filter(servico=ordem.servico)
                            for item in produto_servico:
                                produto = Produto.objects.get(pk=item.produto.pk)
                                produto.quantidade -= item.quantidade
                                produto.save()
                agendamento.status = 'F'
                agendamento.save()
                self.enviar_email(agendamento)
        return agendamento
    
    def enviar_email(self, agendamento):
        email = []
        email.append(agendamento.cliente.email)
        descricao = []
        for servico in agendamento.ordem_servicos_agendamento.all():
            descricao.append(f'{servico} - R$ {servico.preco} ({servico.get_situacao_display()})')

        dados = {
            'cliente': agendamento.cliente.nome,
            'horario': agendamento.horario,
            'funcionario': agendamento.funcionario.nome,
            'descricao': descricao,
            'valor': agendamento.valor,
        }

        texto_email = render_to_string('emails/texto_email.txt', dados)
        html_email = render_to_string('emails/texto_email.html', dados)
        send_mail(
            subject='Lavacar - Serviço concluído',
            message=texto_email,
            from_email='EMAIL@gmail.com',
            recipient_list=email,
            html_message=html_email,
            fail_silently=False,
        )

        return redirect('agendamentos')
