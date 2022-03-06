from django.urls import path
from dashboard import views

urlpatterns = [
    path('index', views.index, name='index'),
    path('charts.html', views.charts, name='charts'),
    path('', views.returnIndex, name='backButton')
]