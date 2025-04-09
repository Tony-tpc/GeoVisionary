from django.urls import path
from .views import (proxy_image, bilibili_outline, baidu_baike, trefle_plants, search_bilibili_videos, get_bilibili_tags,
                    auto_add_baike, auto_add_bilibili)

app_name = 'proxy'
urlpatterns = [
    path('proxy-image/', proxy_image, name='proxy-image'),
    path('bilibili/', bilibili_outline, name='bilibili'),
    path('bilibili-search/', search_bilibili_videos, name='bilibili-search'),
    path('baidu-baike/', baidu_baike, name='baidu-baike'),
    path('trefle-plants/', trefle_plants, name='trefle-plants'),
    path('bilibili-tags/', get_bilibili_tags, name='bilibili-tags'),
    path('auto-add-baike/', auto_add_baike, name='auto_add_baike'),
    path('auto-add-bilibili/', auto_add_bilibili, name='auto_add_bilibili'),
]
