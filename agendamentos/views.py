from .forms import AgendamentoListForm, AgendamentoModelForm
from .models import Agendamento

class AgendamentoView(ListView):
    model = Agendamento
    template_name = 'agendamentos.html'

    def get_context_data(self, **kwargs):
        context = super(AgendamentosView, self).get_context_data(**kwargs)
        if self.request.GET:
            form = AgendamentoListForm()
        context['form'] = form
        return context

    def get_queryset(self):
        qs = super(AgendamentosView, self).get_queryset()
        if self.request.GET:
            form = AgendamentoListForm(self.request.GET)
            if form.is_valid():
                cliente = form.cleaned_data['cliente']
                funcionario = form.cleaned_data['funcionario']
                if cliente:
                    qs = qs.filter(cliente=cliente)
                if funcionario:
                    qs = qs.filter(funcionario=funcionario)

        if qs.count()>0:
            paginator = Paginator(qs, 1)
            listagem = paginator.get_page(self.request.GET.get('page'))
            return listagem
        else:
            return messages.info(self.request, 'Não existem agendamentos cadastrados!')

class AgendamentoAddView(SuccessMessageMixin, CreateView):
    model = Agendamento
    form_class = AgendamentoModelForm
    template_name = 'agendamento_form.html'
    success_url = reverse_lazy('agendamentos')
    success_message = 'Agendamento criado com sucesso!'

class AgendamentoUpdateView(SuccessMessageMixin, UpdateView):
    model = Agendamento
    form_class = AgendamentoModelForm
    template_name = 'agendamento_form.html'
    success_url = reverse_lazy('agendamentos')
    success_message = 'Agendamento atualizado com sucesso!'

class AgendamentoDeleteView(SuccessMessageMixin, DeleteView):
    model = Agendamento
    template_name = 'agendamento_apagar.html'
    success_url = reverse_lazy('agendamentos')
    success_message = 'Agendamento apagado com sucesso!'
