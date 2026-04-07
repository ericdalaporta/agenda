from django import forms
from .models import Cliente


class ClienteModelForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome', 'endereco', 'fone', 'email', 'foto']

        error_messages = {
            'nome': {'required': 'O nome do cliente é um campo obrigatório'},
            'endereco': {'required': 'O endereço do cliente é um campo obrigatório'},
            'fone': {'required': 'O número de telefone do cliente é obrigatório'},
            'email': {'invalid': 'Formato inválido para o e-mail. Exemplo de formato válido: fulano@dominio.com',
                     'unique': 'E-mail já cadastrado'},
        }
