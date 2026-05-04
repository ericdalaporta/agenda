import random

from django.core.management import BaseCommand
from django_seed import Seed
from faker import Faker

from servicos.models import Servico


class Command(BaseCommand):
    help = 'Seed customizado para gerar dados especificos para serviços'

    def handle(self, *args, **kwargs):
        lista_servicos = []
        for i in range(1, 51):
            lista_servicos.append(f'Serviço {i}')
        seeder = Seed.seeder()
        fake = Faker('pt_BR')
        seeder.add_entity(Servico, 50, {
            'nome': lambda x: random.choice(lista_servicos),
            'preco': lambda x: random.uniform(0.01, 100.00),
            'descricao': lambda x: fake.paragraph(nb_sentences=3),

        })

        inserted_pks = seeder.execute()

        self.stdout.write(self.style.SUCCESS(f'Instâncias de Serviço foram criadas com sucesso!'))