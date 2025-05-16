
#EN EL TERMINAL HACER: py manage.py shell y copiar lo siguiente
#

from customers.models import Client

# Crear tenant 1
client1 = Client(
    domain_url='client1.localhost',
    schema_name='client1',
    name='Client 1',
    paid_until='2023-12-31',
    on_trial=True
)
client1.save()

# Crear tenant 2
client2 = Client(
    domain_url='client2.localhost',
    schema_name='client2',
    name='Client 2',
    paid_until='2023-12-31',
    on_trial=False
)
client2.save()