from django.contrib import messages
from django.contrib.messages import SUCCESS
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Q, ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .forms import ServicoModelForm, ProdutosServicoInLine
from .models import Servico

# Create your views here.

class ServicosView(ListView):
    model = Servico
    template_name = 'servicos.html'

    def get_queryset(self):
        buscar = self.request.GET.get('buscar')
        qs = super(ServicosView, self).get_queryset()
        if buscar:
            qs = qs.filter(Q(nome__icontains=buscar)|Q(descricao__icontains=buscar))

        if qs.count() > 0:
            paginator = Paginator(qs, 20)
            listagem = paginator.get_page(self.request.GET.get('page'))
            return listagem
        else:
            return messages.info(self.request, 'Não existem servicos cadastrados!')

class ServicoAddView(SuccessMessageMixin, CreateView):
    model = Servico
    form_class = ServicoModelForm
    template_name = 'servico_form.html'
    success_url = reverse_lazy('servicos')
    success_message = 'Serviços cadastrado com sucesso'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['frm_inline'] = ProdutosServicoInLine(self.request.POST)
        else:
            data['frm_inline'] = ProdutosServicoInLine()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        frm_inline = context['frm_inline']
        with transaction.atomic():
            if frm_inline.is_valid():
                self.object = form.save()
                frm_inline.instance = self.object
                frm_inline.save()
                return super().form_Valid(form)
            else:
                return self.render_to_response(self.get_context_data(form=form))


class ServicoUpdateView(SuccessMessageMixin, UpdateView):
    model = Servico
    form_class = ServicoModelForm
    template_name = 'servico_form.html'
    success_url = reverse_lazy('servicos')
    success_message = 'Serviço alterado com sucesso'

    def get_queryset(self):
        return super().get_queryset().prefetch_related('produtos_servico_servico')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['frm_inline'] = ProdutosServicoInLine(self.request.POST, instance=self.object)
        else:
            data['frm_inline'] = ProdutosServicoInLine(instance=self.object)
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

class ServicoDeleteView(SuccessMessageMixin, DeleteView):
    model = Servico
    template_name = 'servico_apagar.html'
    success_url = reverse_lazy('servicos')
    sucess_message = 'Serviço apagado com sucesso'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, f'O serviço {self.object} não pode ser exclúido. Esse serviço está registrado em ordens de serviço.')
        return redirect(success_url)