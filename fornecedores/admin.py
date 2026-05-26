from django.contrib import admin

from .models import Fornecedor

@admin.register(Fornecedor)
class FornecedorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cpf', 'fone')
    search_fields = ('nome', 'cpf', 'fone')
