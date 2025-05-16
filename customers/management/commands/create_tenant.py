from django.core.management.base import BaseCommand
from tenant_schemas.utils import get_tenant_model, get_tenant_domain_model

class Command(BaseCommand):
    help = 'Create a new tenant'

    def add_arguments(self, parser):
        parser.add_argument('--schema_name', required=True)
        parser.add_argument('--name', required=True)
        parser.add_argument('--domain', required=True)

    def handle(self, *args, **options):
        TenantModel = get_tenant_model()
        DomainModel = get_tenant_domain_model()

        tenant = TenantModel.objects.create(
            schema_name=options['schema_name'],
            name=options['name'],
        )
        
        DomainModel.objects.create(
            domain=options['domain'],
            tenant=tenant,
            is_primary=True
        )

        self.stdout.write(self.style.SUCCESS(f'Tenant {tenant.name} created!'))