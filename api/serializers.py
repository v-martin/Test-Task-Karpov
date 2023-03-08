from rest_framework import serializers
from api.models import Sale, Detail


class SaleSerializer(serializers.ModelSerializer):
    details = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Sale
        fields = ['sale_id', 'date', 'count_pizza', 'count_drink', 'price', 'user_id', 'details']


class DetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Detail
        fields = ['sale_id', 'good', 'price', 'date', 'user_id']
