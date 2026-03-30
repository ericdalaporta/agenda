from django import forms

from .models import Fornecedor

class FornecedorModelForm(forms.ModelForm):
    class Meta:
        model = Fornecedor
        fields = '__all__'

        error_messages = {
            'nome': {'requiered': 'O nome do fornecedor  é um campo obrigatório'},
            'cnpj': {'requiered': 'O Cnpj do fornecedor é um campo obrigatório', 'unique': 'Cnpj já cadastrado'},
            'fone': {'requiered': 'O número do telefone é um campo obrigatório'},
        }