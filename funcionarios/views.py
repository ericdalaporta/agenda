from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from .models import Funcionario
from .forms import FuncionarioForm

class FuncionariosView(ListView):
    model = Funcionario
    template_name = 'funcionarios.html'

    def get_queryset(self):
        buscar = self.request.GET.get('buscar')
        qs = super().get_queryset()

        if buscar:
            qs = qs.filter(nome__icontains=buscar)

        if qs.count() > 0:
            paginator = Paginator(qs, 1)
            listagem = paginator.get_page(self.request.GET.get('page'))
            return listagem
        else:
            messages.info(self.request, 'Nenhum funcionário encontrado')
            return qs

class FuncionarioAddView(SuccessMessageMixin, CreateView):
    model = Funcionario
    form_class = FuncionarioForm
    template_name = 'funcionario_form.html'
    success_url = reverse_lazy('funcionarios')
    success_message = 'Funcionário cadastrado com sucesso!'

class FuncionarioUpdateView(SuccessMessageMixin, UpdateView):
    model = Funcionario
    form_class = FuncionarioForm
    template_name = 'funcionario_form.html'
    success_url = reverse_lazy('funcionarios')
    success_message = 'Funcionário alterado com sucesso!'

class FuncionarioDeleteView(SuccessMessageMixin, DeleteView):
    model = Funcionario
    template_name = 'funcionario_apagar.html'
    success_url = reverse_lazy('funcionarios')
    success_message = 'Funcionário excluído com sucesso!'

class FuncionarioDeleteView(SuccessMessageMixin, DeleteView):
    model = Funcionario
    template_name = 'funcionario_apagar.html'
    success_url = reverse_lazy('funcionarios')
    success_message = 'Funcionário excluído com sucesso!'