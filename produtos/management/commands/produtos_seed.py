import random

from django.core.management import BaseCommand
from django_seed import Seed

from fornecedores.models import Fornecedor
from produtos.models import Produto


class Command(BaseCommand):
    help = 'Seed customizado para gerar dados especificos para produtos'

    def handle(self, *args, **kwargs):
        lista_produtos = []
        for i in range(7, 101):
            lista_produtos.append(f'Produto {i}')
        seeder = Seed.seeder()

        seeder.add_entity(Produto, 94, {
            'nome': lambda x: random.choice(lista_produtos),
            'preco': lambda x: random.uniform(0.01, 100.00),
            'quantidade': lambda x: random.randint(1, 500),
            'fornecedor': lambda x: random.choice(Fornecedor.objects.all())
        })

        inserted_pks = seeder.execute()

        self.stdout.write(self.style.SUCCESS(f'Instâncias de Produto foram criadas com sucesso!'))