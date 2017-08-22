from django.forms.widgets import Select


class ColorSelector(Select):
    template_name = 'widgets/colorpicker_select.html'
    option_template_name = 'widgets/colorpicker_option.html'

    def get_context(self, name, value, attrs):
        context = super(Select, self).get_context(name, value, attrs)
        context['widget']['color'] = value
        return context
