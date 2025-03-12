import jwt
from django.http import JsonResponse
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response  # 使用 DRF 的 Response
from rest_framework.decorators import api_view, parser_classes, permission_classes
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth.hashers import make_password, check_password

from GeoVisionary_Backend import settings
from users.utils.MyJWT import generate_tokens, decode_token

from .models import FrontendUser
from .serializers import FrontendUserSerializer

@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])  # 解析文件上传
def register_user(request):
    """
    处理用户注册请求
    """
    data = request.data
    serializer = FrontendUserSerializer(data=data)
    if not serializer.is_valid():
        return Response({
            'errors':serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    gender = data.get("gender")
    grade = data.get("grade")
    remarks = data.get("desc")
    avatar = request.FILES.get("avatar")  # 获取上传的头像

    # 创建用户，密码加密存储
    user = FrontendUser.objects.create(
        username=username,
        email=email,
        password=make_password(password),  # 使用 Django 自带的加密方法
        gender=gender,
        grade=grade,
        remarks=remarks,
        avatar=avatar,
    )

    # 生成 JWT Token
    access_token, refresh_token = generate_tokens(user)

    # 返回用户信息和 Token
    response_serializer = FrontendUserSerializer(instance=user)
    return Response(
        {
            "user": response_serializer.data,
            "access_token": access_token,
            "refresh_token": refresh_token,
        },
        status=status.HTTP_201_CREATED,
    )

@api_view(['POST'])
def login_user(request):
    """
    处理用户登录请求
    """
    data = request.data
    password = data.get("password")

    # 根据用户名或邮箱查询用户
    user = None
    if data.get("username"):
        user = FrontendUser.objects.filter(username=data.get("username")).first()
    elif data.get("email"):
        user = FrontendUser.objects.filter(email=data.get("email")).first()

    # 验证用户是否存在 & 密码是否正确
    if user and check_password(password, user.password):  # Django 提供的密码校验方法
        access_token, refresh_token = generate_tokens(user)  # 生成 JWT
        serializer = FrontendUserSerializer(user)

        return Response({
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": serializer.data
        }, status=status.HTTP_200_OK)

    return Response({
        "errors": "用户名或密码错误"
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def refresh_token(request):
    refresh_token = request.data.get("refresh_token")
    user_id = decode_token(refresh_token)
    if not user_id:
        return Response({"error": "无效或过期的 refresh_token"}, status=401)

    try:
        user = FrontendUser.objects.get(user_id=user_id)
        access_token, refresh_token = generate_tokens(user)
        return Response({"access_token": access_token, "refresh_token": refresh_token})
    except FrontendUser.DoesNotExist:
        return Response({"error": "用户不存在"}, status=401)


@api_view(["POST"])
@permission_classes([AllowAny])  # 允许所有用户访问
def auto_login(request):
    """
    通过 access_token 自动登录（不使用 SimpleJWT）
    """
    token = request.data.get("access_token")
    if not token:
        return Response({"error": "缺少 access_token"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # 使用 PyJWT 解码 access_token
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id = decoded_token.get("user_id")  # 获取 user_id
        if not user_id:
            return Response({"error": "Token 无效"}, status=status.HTTP_401_UNAUTHORIZED)

        # 查询用户
        user = FrontendUser.objects.get(user_id=user_id)
        serializer = FrontendUserSerializer(user)

        return Response({
            "message": "Token 验证成功",
            "user": serializer.data
        }, status=status.HTTP_200_OK)

    except jwt.ExpiredSignatureError:
        return Response({"error": "Token 已过期"}, status=status.HTTP_401_UNAUTHORIZED)
    except jwt.InvalidTokenError:
        return Response({"error": "Token 无效"}, status=status.HTTP_401_UNAUTHORIZED)
    except FrontendUser.DoesNotExist:
        return Response({"error": "用户不存在"}, status=status.HTTP_404_NOT_FOUND)

@api_view(["GET"])
def leaderboard_inquiry(request):
    user_list = FrontendUser.objects.all()
    response_dict = {}
    for obj in user_list:
        response_dict[obj.username] = {
            'correct_problems': obj.correct_problems,
            'avatar': request.build_absolute_uri(obj.avatar.url) if obj.avatar else None  # 生成完整URL
        }
    return JsonResponse({"user_object": response_dict},status=status.HTTP_200_OK)
