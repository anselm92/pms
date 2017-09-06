from captcha.fields import ReCaptchaField
from django.core.exceptions import ValidationError
from django.forms import ModelForm, CharField, EmailField, CheckboxInput, BooleanField, HiddenInput

from printing.models import Order, Material, Comment, StaffComment, ExternalComment, Customer, ExternalCustomer, \
    ORDER_STATUS_OPEN


class OrderBaseForm(ModelForm):
    class Meta:
        model = Order
        fields = ['title', 'amount', 'file']


class MaterialBaseForm(ModelForm):
    class Meta:
        model = Material
        fields = ['name']


class CommentBaseForm(ModelForm):
    subscribe_for_notifications = BooleanField(required=False)

    class Meta:
        model = Comment
        fields = ['text']


class StaffCommentBaseForm(CommentBaseForm):
    class Meta(CommentBaseForm.Meta):
        model = StaffComment
        fields = CommentBaseForm.Meta.fields + ['public']


class ExternalCustomerForm(ModelForm):
    captcha = ReCaptchaField(attrs={'theme': 'clean'})

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


class CancelOrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['status']
        widgets = {'status': HiddenInput()}

    def clean_status(self):
        status = self.cleaned_data['status']
        if self.instance.status != ORDER_STATUS_OPEN:
            raise ValidationError("Cannot cancel an order whichs state is not open")
        return status
