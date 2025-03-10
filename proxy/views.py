import json
import os

import httpx
import requests
from django.http import HttpResponse, JsonResponse, StreamingHttpResponse, HttpRequest
from django.utils.encoding import force_bytes
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv
from rest_framework.decorators import api_view
import asyncio
from .websocket_client import send_to_tts

load_dotenv()
DS_MODEL = os.environ.get("DS_MODEL")
DS_KEY = os.environ.get("DS_KEY")

# 代理图片请求
@api_view(["GET"])
def proxy_image(request):
    image_url = request.GET.get('url')
    if not image_url:
        return HttpResponse("缺少图片 URL 参数", status=400)

    try:
        response = requests.get(image_url)
        response.raise_for_status()  # 如果请求失败，抛出异常

        # 创建 HTTP 响应，设置内容类型和内容
        http_response = HttpResponse(response.content)
        # 设置内容类型为从请求中获取的图片的内容类型
        http_response['Content-Type'] = response.headers.get('Content-Type', 'image/jpeg')
        return http_response
    except requests.RequestException as error:
        print("代理图片失败:", error)
        return HttpResponse("无法获取图片", status=500)

# 代理 bilibili(可分p) API 请求
def bilibili(request):
    # 获取 BV 号和分p
    bvid = request.GET.get('bvid')
    p = request.GET.get('p')
    if not bvid or not p:
        return HttpResponse("请提供 BV 号和页码", status=400)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    }

    try:
        # 获取所有分P的 cid
        pagelist_url = f'https://api.bilibili.com/x/player/pagelist?bvid={bvid}'
        pagelist_response = requests.get(pagelist_url, headers=headers)
        pagelist_json = pagelist_response.json()

        if pagelist_json.get("code") != 0:
            return HttpResponse(f"Bilibili API 错误: {pagelist_json.get('message')}", status=500)

        pagelist = pagelist_json.get("data", [])
        if not pagelist:
            return HttpResponse('找不到分p数据', status=404)

        # 找到参数p对应的 cid
        index = int(p) - 1
        if index < 0 or index >= len(pagelist):
            return HttpResponse('页码超出范围', status=400)

        cid = pagelist[index]['cid']

        # 获取具体P的视频信息
        view_url = f'https://api.bilibili.com/x/web-interface/view?bvid={bvid}&cid={cid}'
        view_response = requests.get(view_url, headers=headers)
        view_json = view_response.json()

        if view_json.get("code") != 0:
            return HttpResponse(f"Bilibili API 错误: {view_json.get('message')}", status=500)
        response = JsonResponse(view_json, content_type='application/json')
        response["Access-Control-Allow-Origin"] = "*"
        return response

    except requests.RequestException as error:
        print('代理请求 Bilibili API 失败', error)
        return HttpResponse('获取数据失败', status=500)
