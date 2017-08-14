from django.forms import ModelForm

from printing.models import Order, Material, Comment, StaffComment


class OrderBaseForm(ModelForm):
    class Meta:
        model = Order
        fields = ['title', 'amount']


class MaterialBaseForm(ModelForm):
    class Meta:
        model = Material
        fields = ['name']


class CommentBaseForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text']


class StaffCommentBaseForm(ModelForm):
    class Meta:
        model = StaffComment
        fields = ['text', 'public']
