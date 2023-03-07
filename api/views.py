from celery.result import AsyncResult
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import viewsets, status
from api.models import Detail
from api.utils import get_model_map, get_serializer_map
from TestTask.celery import app as celery_app
from api.tasks import calculate_metric


class Logs(viewsets.ReadOnlyModelViewSet):

    def list(self, request, *args, **kwargs):
        min_date = Detail.objects.earliest('date').date
        since = min_date
        table_type = request.query_params.get('table_name')
        if not table_type:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'table_type': 'There are tables Sale and Detail'})
        model = get_model_map().get(table_type)
        if not model:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'table_type': 'Non existent'})
        if 'from_date' in request.query_params:
            since = request.query_params['from_date']
        if 'user_id' in request.query_params:
            queryset = model.objects.filter(date__gte=since,
                                            user_id=request.query_params['user_id']).order_by('-sale_id')[:100:-1]
        else:
            queryset = model.objects.filter(date__gte=since).order_by('-sale_id')[:100:-1]
        serializer = get_serializer_map().get(table_type + 'Serializer')
        serializer = serializer(queryset, many=True)
        return Response(serializer.data)


@api_view(["PUT"])
def launch(request: Request, *args, **kwargs) -> HttpResponse:
    result = calculate_metric.delay()
    print(result.as_list())
    return JsonResponse(
        {
            "task_id": result.as_list()[-1]
        }
    )


@api_view(["GET"])
def get_result(request: Request, *args, **kwargs) -> HttpResponse:
    task_id = request.query_params.get('job_id')
    if not task_id:
        return Response(status=status.HTTP_400_BAD_REQUEST, data={
            "detail": "job_id not found"
        })
    res = AsyncResult(task_id, app=celery_app)
    state = res.state
    if state == 'PENDING':
        return Response(status=status.HTTP_400_BAD_REQUEST, data={
            "detail": "invalid job_id"
        })
    return JsonResponse(
        {
            "status": state,
            "result": res.get() if state == "SUCCESS" else None
        }
    )