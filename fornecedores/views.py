from django.contrib import messages
from django.contrib.messages import SUCCESS
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .forms import FornecedorModelForm
from .models import Fornecedor
from django.views.generic.base import TemplateResponseMixin, View
from django.contrib.auth.mixins import PermissionRequiredMixin

# Create your views here.

class FornecedoresView(PermissionRequiredMixin, ListView):
    model = Fornecedor
    template_name = 'fornecedores.html'
    permission_required = 'fornecedores.view_fornecedor'
    permission_denied_message = 'Visualizar fornecedores'

    def get_queryset(self):
        buscar = self.request.GET.get('buscar')
        qs = super(FornecedoresView, self).get_queryset()
        if buscar:
            return qs.filter(nome__icontains=buscar)

        if qs.count() > 0:
            paginator = Paginator(qs, 20)
            listagem = paginator.get_page(self.request.GET.get('page'))
            return listagem
        else:
            return messages.info(self.request, 'Não existem fornecedores cadastrados!')

class FornecedorAddView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = 'fornecedores.add_fornecedor'
    permission_denied_message = 'Cadastrar fornecedor'
    model = Fornecedor
    form_class = FornecedorModelForm
    template_name = 'fornecedor_form.html'
    success_url = reverse_lazy('fornecedores')
    success_message = 'Fornecedor cadastrado com sucesso'

class FornecedorUpdateView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = 'fornecedores.change_fornecedor'
    permission_denied_message = 'Editar fornecedor'
    model = Fornecedor
    form_class = FornecedorModelForm
    template_name = 'fornecedor_form.html'
    success_url = reverse_lazy('fornecedores')
    success_message = 'Fornecedor alterado com sucesso'

class FornecedorDeleteView(PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    permission_required = 'fornecedores.delete_fornecedor'
    permission_denied_message = 'Excluir fornecedor'
    model = Fornecedor
    template_name = 'fornecedor_apagar.html'
    success_url = reverse_lazy('fornecedores')
    sucess_message = 'Fornecedor apagado com sucesso'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, f'O fornecedor {self.object} não pode ser excluído. Esse fornecedor está registrado no fornecimento de produtos.')
        return redirect(success_url)