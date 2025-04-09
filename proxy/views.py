import os
import time

import requests
from django.http import HttpResponse, JsonResponse
from dotenv import load_dotenv
from rest_framework.decorators import api_view

from users.models import TextContent, RecommendationContent, Category, Video

load_dotenv()
DS_MODEL = os.environ.get("DS_MODEL")
DS_KEY = os.environ.get("DS_KEY")
BAIDU_Key = os.environ.get("BAIDU_KEY")
Trefle_Key = os.environ.get("TREFLE_KEY")

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
def bilibili_outline(request):
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

@api_view(['GET'])
def search_bilibili_videos(request):
    keyword = request.GET.get('keyword')
    if not keyword:
        return JsonResponse({'error': '请输入关键词'}, status=400)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'Cookie': "buvid3=21F3AC10-9306-9633-3A45-5EE38144EF0463518infoc; b_nut=1724649063; _uuid=DBE94810A-F131-D7DF-8AD2-C453FE101D9C270112infoc; buvid4=3B6F114A-4356-F493-8001-75052321C38D64510-024082605-wFeebawqsGB6nzPm83ZA6w%3D%3D; rpdid=|(umu)~|~l)R0J'u~kRYRm|YR; fingerprint=b23632fbc792c3a63491240e96639cc4; buvid_fp_plain=undefined; buvid_fp=b23632fbc792c3a63491240e96639cc4; CURRENT_FNVAL=4048"
    }

    params = {
        'search_type': 'video',
        'keyword': keyword,
    }

    try:
        time.sleep(3)
        response = requests.get(
            'https://api.bilibili.com/x/web-interface/search/type',
            headers=headers,
            params=params
        )
        response.raise_for_status()
        return JsonResponse(response.json())
    except requests.RequestException as e:
        return JsonResponse({'error': str(e)}, status=500)

@api_view(['GET'])
def get_bilibili_tags(request):
    bvid = request.GET.get('bvid')
    if not bvid:
        return JsonResponse({'error': '请输入视频 bvid 号'}, status=400)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    }

    try:
        response = requests.get(
            f'https://api.bilibili.com/x/tag/archive/tags?bvid={bvid}',
            headers=headers,
        )
        response.raise_for_status()
        return JsonResponse(response.json())
    except requests.RequestException as e:
        return JsonResponse({'error': str(e)}, status=500)

@api_view(["GET"])
def baidu_baike(request):
    key_word = request.GET.get('keyword')
    if not key_word:
        return HttpResponse("请提供关键词",status=400)

    try:
        baidu_url = f'https://baike.baidu.com/api/openapi/BaikeLemmaCardApi?appid={BAIDU_Key}&bk_key={key_word}'
        baidu_response = requests.get(baidu_url)
        baidu_json = baidu_response.json()
        if baidu_json.get("errno"):
            return HttpResponse(f"请求 Baidu 百科 API 时发生错误", status=500)

    except requests.RequestException as error:
        print(error)
        return HttpResponse('获取百科内容失败', status=500)
    return JsonResponse(baidu_json, content_type='application/json')

@api_view(["POST","GET"])
def trefle_plants(request):
    query_string = request.data.get('query_string')
    filter_dict = request.data.get("filterDict")
    """
    filterDict = {
        filterType: {typeName: ...,valueList:[...values]}
    }
    """
    raw_url = f"https://trefle.io/api/v1/plants?token={Trefle_Key}"
    if not filter_dict and not query_string:
        response = requests.get(raw_url)
        response.raise_for_status()
        return JsonResponse(response.json(), status=200)

    elif query_string:
        url = raw_url + "&q=" + query_string
        response = requests.get(url)
        response.raise_for_status()
        return JsonResponse(response.json(), status=200)

    elif filter_dict:
        for key, value in filter_dict.items():
            filter_type = key
            type_name = value.get('typeName')
            value_list = value.get('valueList')
            url = f"{raw_url}&{filter_type}[{type_name}]={value_list}"
            response = requests.get(url)
            response.raise_for_status()
            return JsonResponse(response.json(), status=200)

@api_view(['GET'])
def auto_add_baike(request):
    keywords = [
        # 新增自然地理类
        # '气候类型', '大气环流', '洋流',
        # '生态系统', '地质构造', '土壤类型', '自然灾害',
        # '地球运动', '太阳辐射', '黄赤交角', '晨昏线',
        # '二十四节气', '五带划分', '大气分层', '国际日期变更线',

        # 新增人文地理类
        # '城市化', '人口迁移', '交通区位', '可持续发展',
        # '城市结构', '土地利用', '农业区位', '工业区位',
        # '人口政策', '碳达峰', '碳中和',

        # 新增综合技能类
        # '等高线', '时区计算', '太阳高度角',
        # '地理信息技术', '资源评价'
    ]

    for keyword in keywords:
        response = requests.get('http://localhost:8040/proxy/baidu-baike/?keyword=' + keyword)
        response.raise_for_status()
        response_data = response.json()
        keyword_abstract = response_data.get('abstract','')
        TextContent.objects.get_or_create(keyword=keyword,description=keyword_abstract)
        RecommendationContent.objects.get_or_create(content_type='text',content_key=keyword)
        print(keyword)

    return JsonResponse({"data":"数据更新完成！"}, status=200)


@api_view(['GET'])
def auto_add_bilibili(request):
    bvid = input('请输入bvid:\n')
    while bvid != '':
        print(bvid)
        p = input('请输入分p编号:\n')
        title = input('请输入标题:\n')
        description = input('请输入描述:\n')
        topic = input('请输入考点:\n')
        category = Category.objects.filter(category_type='topic',name=topic).first()
        print(category)
        Video.objects.get_or_create(bvid=bvid,title=title,description=description,topic=category, p=p)
        RecommendationContent.objects.get_or_create(content_type='video',content_key=(bvid + '-1'),category=category)
        bvid = input('请输入bvid:\n')

    return JsonResponse({"data": 'ok'}, status=200)