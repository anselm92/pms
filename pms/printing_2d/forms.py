from printing.forms import OrderBaseForm
from printing.widgets import ColorSelector
from printing_2d.models import ScriptOrder, CustomOrder2d


class ScriptOrderForm(OrderBaseForm):
    class Meta(OrderBaseForm.Meta):
        model = ScriptOrder
        fields = OrderBaseForm.Meta.fields + ['cover_sheet_color']
        widgets = {
            'cover_sheet_color': ColorSelector(),
        }


class CustomOrder2dForm(OrderBaseForm):
    class Meta(OrderBaseForm.Meta):
        model = CustomOrder2d
        fields = OrderBaseForm.Meta.fields + ['cost_center','sided_printing', 'chromatic_printing', 'post_processing', 'material']
