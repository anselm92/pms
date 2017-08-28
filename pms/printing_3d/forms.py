from printing.forms import OrderBaseForm
from .models import Order3d


class Order3dForm(OrderBaseForm):
    class Meta(OrderBaseForm.Meta):
        model = Order3d
        fields = OrderBaseForm.Meta.fields + ['material', 'width', 'height', 'depth']
