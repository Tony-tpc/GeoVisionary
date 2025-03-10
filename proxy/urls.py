from django.urls import path
from .views import proxy_image, bilibili

app_name = 'proxy'
urlpatterns = [
    path('proxy-image/', proxy_image, name='proxy-image'),
    path('bilibili/', bilibili, name='bilibili'),
]
