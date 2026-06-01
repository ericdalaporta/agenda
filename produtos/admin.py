from django.contrib import admin

from .models import Produto

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'preco', 'quantidade', 'fornecedor')

    search_fields = ('nome',)
    list_filter = ('fornecedor',)