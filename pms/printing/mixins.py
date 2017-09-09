from django.contrib.auth.mixins import AccessMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy

from printing.models import Configuration


class PermissionPostGetRequiredMixin(AccessMixin):
    """
    CBV mixin which verifies that the current user has all specified
    permissions.
    """
    permission_post_required =[]
    permission_get_required = []

    def get_permission_required(self, method):
        perms=[]
        if method == 'POST':
            perms+=self.permission_post_required
        else:
            perms+= self.permission_get_required
        return perms

    def has_permission(self, method):
        perms = self.get_permission_required(method)
        return self.request.user.has_perms(perms)

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission(request.method):
            return self.handle_no_permission()
        return super(PermissionPostGetRequiredMixin, self).dispatch(request, *args, **kwargs)


class MaintenanceMixin(object):
    maintenance_url = reverse_lazy('printing:maintenance')

    def is_maintenance_enabled(self):
        config = Configuration.objects.all().first()
        return config.maintenance

    def dispatch(self, request, *args, **kwargs):
        if self.is_maintenance_enabled():
            return redirect(self.maintenance_url)
        return super(MaintenanceMixin, self).dispatch(request, *args, **kwargs)
