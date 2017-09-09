from django import template
from django.urls import resolve

register = template.Library()

@register.simple_tag
def user_can_see_view(view, user):
    view_o = resolve(view)
    view_class = view_o.func.view_class
    has_attr = hasattr(view_class,'permission_get_required')
    if has_attr:
        return user.has_perms(getattr(view_class,'permission_get_required'))
    else:
        return True


