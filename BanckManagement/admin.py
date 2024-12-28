from django.contrib import admin
from BanckManagement.models import *


# Register your models here.

admin.site.register(BankAccount)
admin.site.register(InvastMents)
admin.site.register(Deposite)
admin.site.register(PayOut)
admin.site.register(WaletShate)
admin.site.register(TradePackeges)
admin.site.register(GetReward)
admin.site.register(PaymentMethod)

