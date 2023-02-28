from rest_framework.response import Response
from rest_framework import viewsets
from api.models import Sale, Detail, model_string_map
from api.serializers import SaleSerializer, DetailSerializer, model_serializer_map

min_date = Detail.objects.earliest('date').date


class Logs(viewsets.ReadOnlyModelViewSet):
    # permission_classes = []

    def list(self, request, *args, **kwargs):
        table_type = request.query_params['table_name']
        model = model_string_map.get(table_type)
        since = min_date
        if 'from_date' in request.query_params:
            since = request.query_params['from_date']
            print(since)
        if 'user_id' in request.query_params:
            queryset = model.objects.filter(date=since,
                                            user_id=request.query_params['user_id']).order_by('-sale_id')[:100:-1]
        else:
            queryset = model.objects.filter(date=since).order_by('-sale_id')[:100:-1]
        serializer = model_serializer_map.get(table_type + 'Serializer')
        serializer = serializer(queryset, many=True)
        return Response(serializer.data)



