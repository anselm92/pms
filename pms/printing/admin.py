from django.contrib import admin
from .models import *

admin.site.register(StaffCustomer)
admin.site.register(ExternalCustomer)
admin.site.register(CostCenter)
admin.site.register(StaffComment)
admin.site.register(ExternalComment)
admin.site.register(Subscription)
admin.site.register(OrderHistoryStaffEntry)
admin.site.register(OrderHistoryExternalEntry)
admin.site.register(CustomGroupFilter)
admin.site.register(OrderHistoryEntry)
admin.site.register(Configuration)
