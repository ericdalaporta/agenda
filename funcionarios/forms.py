from django import forms

from .models import Funcionario

class FuncionarioForm(forms.ModelForm):

    class Meta:
        model = Funcionario
        fields = ['nome', 'funcao', 'fone', 'email', 'data_admissao', 'foto']

        error_messages = {
            'nome': {'required': 'O nome do funcionário é um campo obrigatório'},
            'funcao': {'required': 'A função do funcionário é um campo obrigatório'},
            'fone': {'required': 'O telefone do funcionário é um campo obrigatório'},
            'email': {'required': 'O email do funcionário é um campo obrigatório', 'invalid': 'Formato inválido para o e-mail. Exemplo de formato válido: fulano@dominio.com',
            'unique': 'Este e-mail já cadastrado'},
        }