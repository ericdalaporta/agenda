from django.db import models
from django.db.models.functions import Upper

from stdimage.models import StdImageField

class Pessoa(models.Model):
    nome = models.CharField('Nome', max_length=50, help_text='Nome completo')
    fone = models.CharField('Fone', max_length=20, blank=True, help_text='Telefone de contato')
    email = models.EmailField('E-mail', blank=True, help_text='Endereço de e-mail')
    foto = StdImageField('Foto', upload_to='Foto', blank=True, null=True, help_text='Foto do cliente')

    class Meta:
        abstract = True

    def __str__(self):
        return self.nome

class Cliente(Pessoa):
    endereco = models.CharField('Endereço', max_length=100, blank=True, help_text='Endereço Completo')

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

    def __str__(self):
        return self.nome