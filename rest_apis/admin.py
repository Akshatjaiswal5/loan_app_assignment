from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(TransactionRecord)
admin.site.register(Loan)
admin.site.register(EMI)
admin.site.register(Payment)
