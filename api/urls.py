from django.urls import path

from api import views

urlpatterns = [
    path('logs', views.Logs.as_view({'get': 'list'})),
    path('launch', views.launch),
    path('get_result', views.get_result)
]