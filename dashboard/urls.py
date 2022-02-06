from django.urls import path
from dashboard import views

urlpatterns = [
    path('index', views.index, name='index'),
    path('acceptFips', views.acceptFips, name='fips'),
    path('charts', views.charts, name='charts'),
    path('', views.returnIndex, name='backButton')
]