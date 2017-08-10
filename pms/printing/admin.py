from django.contrib import admin
from .models import *

admin.site.register(StaffCustomer)
admin.site.register(ExternalCustomer)
admin.site.register(CostCenter)
admin.site.register(StaffComment)
admin.site.register(ExternalComment)
