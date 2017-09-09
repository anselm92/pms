from django.contrib.auth.models import User
from rest_framework import serializers, viewsets
from rest_framework.parsers import MultiPartParser, FormParser

from printing.models import Order, Customer


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        # fields = ('url', 'username', 'email', 'is_staff')


# ViewSets define the view behavior.
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().select_subclasses()
    serializer_class = OrderSerializer
    parser_classes = (MultiPartParser, FormParser,)

    def perform_create(self, serializer):
        #serializer.save(datafile=self.request.data.get('file'))
        super(viewsets.ModelViewSet, self).perform_create(serializer)

        # def perform_create(self, serializer):
        #     serializer.save(owner=self.request.user,
        #                    datafile=self.request.data.get('datafile'))


class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


# ViewSets define the view behavior.
class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Routers provide an easy way of automatically determining the URL conf.
