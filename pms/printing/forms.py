from captcha.fields import ReCaptchaField
from django.forms import ModelForm, CharField, EmailField

from printing.models import Order, Material, Comment, StaffComment, ExternalComment, Customer, ExternalCustomer


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


class ExternalCustomerForm(ModelForm):
    #captcha = ReCaptchaField()

    class Meta:
        model = ExternalCustomer
        fields = ['first_name', 'last_name', 'mail_address']


class ExternalCommentForm(CommentBaseForm, ExternalCustomerForm):
    first_name = CharField(max_length=20)
    last_name = CharField(max_length=20)
    mail_address = EmailField()

    class Meta(CommentBaseForm.Meta):
        model = ExternalComment
        fields = ExternalCustomerForm.Meta.fields + CommentBaseForm.Meta.fields
