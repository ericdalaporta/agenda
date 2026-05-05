from django.db import models

from clientes.models import Cliente


class Agendamento(models.Model):
    horario = models.DateTimeField('Horário', help_text='Data e hora do atendimento')
    cliente = models.ForeignKey('clientes.Cliente', verbose_name="Cliente", help_text="Nome do cliente", on_delete=models.PROTECT)
    funcionario = models.ForeignKey('funcionarios.Funcionario', verbose_name="Funcionário", help_text="Nome do funcionário", on_delete=models.PROTECT)
    servicos = models.ManyToManyField('servicos.Servico', verbose_name='Serviço', through='agendamentos.OrdemServicos')

    class Meta:
        verbose_name = 'Agendamento'
        verbose_name_plural = 'Agendamentos'

    def __str__(self):
        return f'Cliente: {self.cliente}'

class OrdemServicos(models.Model):
    SITUACAO_OPCOES = (
        ('A', 'Agendado'),
        ('B', 'Realizado'),
        ('C', 'Cancelado'),
    )

    agendamento = models.ForeignKey('agendamentos.Agendamento', verbose_name="Agendamento", on_delete=models.PROTECT, related_name='ordem_servicos_agendamento')
    servico = models.ForeignKey('servicos.Servico', verbose_name='Serviço', on_delete=models.PROTECT, related_name='ordem_servicos_servico')
    funcionario = models.ForeignKey('funcionarios.Funcionario', verbose_name="Funcionário", on_delete=models.PROTECT, related_name='ordem_servicos_funcionario')

    situacao = models.CharField(max_length=1, choices=SITUACAO_OPCOES, default='A')
    observacoes = models.TextField('Observações', max_length=300, blank=True, null=True)

    preco = models.DecimalField('Preço', max_digits=6, decimal_places=2, help_text='Preço do serviço', default=0.00)

    class Meta:
        verbose_name = 'Serviço realizado'
        verbose_name_plural = 'Serviços realizados'

        constraints = [
            models.UniqueConstraint(fields=['agendamento', 'servico'], name='constraint_agendamento')
        ]

    def __str__(self):
        return self.servico.nome