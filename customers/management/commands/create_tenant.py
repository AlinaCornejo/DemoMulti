from django.core.management.base import BaseCommand
from tenant_schemas.models import TenantMixin
from django.db import connection

class Command(BaseCommand):
    help = 'Creates a new tenant'

    def add_arguments(self, parser):
        parser.add_argument('--schema_name', required=True)
        parser.add_argument('--name', required=True)
        parser.add_argument('--domain', required=True)

    def handle(self, *args, **options):
        from customers.models import Client, Domain  # Asegúrate de importar tus modelos
        
        tenant = Client.objects.create(
            schema_name=options['schema_name'],
            name=options['name'],
            domain_url=options['domain']
        )

        self.stdout.write(self.style.SUCCESS(f'Tenant {tenant.name} created successfully!'))