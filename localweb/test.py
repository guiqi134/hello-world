import os
import django
from catalog.models import Account

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'localweb.settings')
django.setup()

print(Account.objects.filter(account_type__contains='customer'))
