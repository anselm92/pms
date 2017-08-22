from django.forms import ModelForm

from printing.models import Order, Material, Comment, StaffComment, ExternalComment


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


class StaffCommentBaseForm(CommentBaseForm):
    class Meta(CommentBaseForm.Meta):
        model = StaffComment
        fields = CommentBaseForm.Meta.fields + ['public']


class ExternalCommentForm(CommentBaseForm):
    class Meta(CommentBaseForm.Meta):
        model = ExternalComment
        fields = CommentBaseForm.Meta.fields
