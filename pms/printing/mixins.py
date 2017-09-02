from django.contrib.auth.mixins import AccessMixin


class PermissionPostGetRequiredMixin(AccessMixin):
    """
    CBV mixin which verifies that the current user has all specified
    permissions.
    """
    permission_post_required = ''
    permission_get_required = ''

    def get_permission_required(self, method):
        if method == 'POST':
            perms = self.permission_post_required
        else:
            perms = self.permission_get_required
        return perms

    def has_permission(self,method):
        perms = self.get_permission_required(method)
        return self.request.user.has_perms(perms)

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission(request.method):
            return self.handle_no_permission()
        return super(PermissionPostGetRequiredMixin, self).dispatch(request, *args, **kwargs)