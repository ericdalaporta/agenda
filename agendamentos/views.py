from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.db import transaction
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .forms import AgendamentoListForm, AgendamentoModelForm, \
    AgendamentosServicoInLine
from .models import Agendamento


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