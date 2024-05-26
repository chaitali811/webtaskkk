from django.contrib import admin


from webhook_app.models import Account
from webhook_app.models import Destination

admin.site.register(Account)
admin.site.register(Destination)