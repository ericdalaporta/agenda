from django.db import models

# Create your models here.
class Servico(models.Model):
    nome = models.CharField("Nome", max_length=100, help_text="Nome do serviço", unique=True)
    preco = models.DecimalField("Preço",max_digits=5, decimal_places=2, help_text="Preço do serviço")
    descricao = models.CharField("Descrição do serviço", max_length=300, help_text="Descrição do serviço")
    produtos = models.ManyToManyField('produtos.Produto',through='servicos.ProdutosServico', related_name='servicos_produtos')

    class Meta:
        verbose_name = "Serviço"
        verbose_name_plural = "Serviços"

    def __str__(self):
        return self.nome

class ProdutosServico(models.Model):
    servico = models.ForeignKey('servicos.Servico', verbose_name="Serviço", on_delete=models.CASCADE, related_name='produtos_servico_servico')
    produto = models.ForeignKey('produtos.Produto', verbose_name="Produto", on_delete=models.PROTECT, related_name='produtos_produto_servico')
    quantidade = models.DecimalField('Quantidade', max_digits=5, decimal_places=2)

    class Meta:
        verbose_name = 'Produto utilizado'
        verbose_name_plural = 'Produtos utilizados'

    def __str__(self):
        return f'{self.produto}'