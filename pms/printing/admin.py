from django.contrib import admin
from .models import *

admin.site.register(Customer)
admin.site.register(StaffCustomer)
admin.site.register(CostCenter)
admin.site.register(Order)
admin.site.register(Material)
admin.site.register(Comment)
admin.site.register(StaffComment)
admin.site.register(ExternalComment)
