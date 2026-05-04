import random

from django.core.management import BaseCommand
from django_seed import Seed

from produtos.models import Produto
from servicos.models import Servico, ProdutosServico



class Command(BaseCommand):
    help = 'Seed customizado para gerar dados específicos para produtos utilizados em serviços'

    def handle(self, *args, **kwargs):
        seeder = Seed.seeder()
        seeder.add_entity(ProdutosServico, 40, {
            'servico': lambda x: random.choice(Servico.objects.all()),
            'produto': lambda x: random.choice(Produto.objects.all()),
            'quantidade': lambda x: random.uniform(0.01, 100.00),
        })

        inserted_pks = seeder.execute()

        self.stdout.write(self.style.SUCCESS(f'Instâncias de Produtos utilizados em Serviços foram criadas com suceso!'))