from rest_framework import serializers
from api.models import Sale, Detail
import inspect
import sys


class SaleSerializer(serializers.ModelSerializer):
    details = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Sale
        fields = ['sale_id', 'date', 'count_pizza', 'count_drink', 'price', 'user_id', 'details']


class DetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Detail
        fields = ['sale_id', 'good', 'price', 'date', 'user_id']


model_serializer_map = {}
for cls_name, cls_obj in inspect.getmembers(sys.modules[__name__]):
    if inspect.isclass(cls_obj):
        model_serializer_map.update({cls_name: cls_obj})
