from decimal import Decimal
from django.core.management.base import BaseCommand
from django.utils import timezone
from django_seed import Seed
from agendamentos.models import Agendamento, OrdemServicos
from clientes.models import Cliente
from funcionarios.models import Funcionario
from random import randint, choice
from servicos.models import Servico


class Command(BaseCommand):
    help = 'Seed customizado para gerar dados específicos para agendamentos'

    def handle(self, *args, **kwargs):
        seeder = Seed.seeder()

        clientes = list(Cliente.objects.all())
        funcionarios = list(Funcionario.objects.all())
        servicos = list(Servico.objects.all())

        if not clientes or not funcionarios or not servicos:
            self.stdout.write(self.style.ERROR(
                'É necessário ter clientes, funcionários e serviços cadastrados antes de rodar o seed.'
            ))
            return

        agendamentos = []

        for _ in range(1, 11):
            agendamento = Agendamento.objects.create(
                horario=timezone.now() + timezone.timedelta(
                    days=randint(0, 7),
                    hours=randint(8, 18)
                ),
                cliente=choice(clientes),
                funcionario=choice(funcionarios),
                valor=Decimal('0.00'),
                status='A',
            )
            agendamentos.append(agendamento)

        for agendamento in agendamentos:
            num_servicos = randint(1, 4)
            servicos_escolhidos = [choice(servicos) for _ in range(num_servicos)]

            for servico in servicos_escolhidos:
                OrdemServicos.objects.create(
                    agendamento=agendamento,
                    servico=servico,
                    funcionario=agendamento.funcionario,
                    situacao='A',
                    observacoes='Agendado automaticamente',
                    preco=servico.preco,
                )

        self.stdout.write(self.style.SUCCESS('Instâncias foram criadas com sucesso!'))