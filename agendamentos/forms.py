from django import forms
from django.forms import inlineformset_factory
from tempus_dominus.widgets import DatePicker

from agendamentos.models import Agendamento, OrdemServicos
from clientes.models import Cliente
from funcionarios.models import Funcionario


class AgendamentoListForm(forms.Form):
    cliente = forms.ModelChoiceField(label='Cliente', queryset=Cliente.objects.all(), required=False)
    funcionario = forms.ModelChoiceField(label='Funcionário', queryset=Funcionario.objects.all(), required=False)

class AgendamentoModelForm(forms.ModelForm):
    class Meta:
        model = Agendamento
        fields = ['horario', 'cliente', 'funcionario']
        widgets = {
            'horario': forms.DateTimeInput(
                format='%Y-%m-%dT%H:%M',
                attrs={'type': 'datetime-local' ,'class': 'form-control'}
            ),
        }

        error_messages = {
            'horario': {'required': 'O horário é um campo obrigatório'},
            'cliente': {'required': 'O cliente é um campo obrigatório'},
            'funcionario': {'required': 'O funcionário é um campo obrigatório'},
        }

AgendamentosServicoInLine = inlineformset_factory(
    Agendamento, OrdemServicos, fields=('servico', 'funcionario', 'situacao', 'observacoes'),
    extra=1,
    can_delete=True
)