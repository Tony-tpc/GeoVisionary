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
from django.db.models import Prefetch
from .models import FrontendUser, Problem, ExamSet, Category
from .serializers import FrontendUserSerializer, ProblemSerializer, ExamSetSerializer

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
    通过 access_token 自动登录
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

@api_view(["POST"])
@parser_classes([MultiPartParser, FormParser])  # 解析文件上传
def update_user(request):
    """
    用户信息更新接口
    """
    # user = request.user  # 通过JWT认证获取用户
    # 处理文件上传
    # print(user)
    # avatar_file = request.FILES.get("avatar")
    token = request.data.get("access_token")
    if not token:
        return Response(
            {"error": "缺少 access_token"}, status=status.HTTP_400_BAD_REQUEST
        )
    try:
        # 使用 PyJWT 解码 access_token
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id = decoded_token.get("user_id")  # 获取 user_id
        if not user_id:
            return Response(
                {"error": "Token 无效"}, status=status.HTTP_401_UNAUTHORIZED
            )
        user = FrontendUser.objects.get(user_id=user_id)
        update_data = request.data.copy()

        # 生成排除字段集合
        excluded_fields = {"access_token"} | {
            field
            for field in update_data
            if field != "avatar"  # 跳过头像字段
            and (
                update_data[field] in (None, "", "null")  # 空值检查
                or str(update_data[field])
                == str(getattr(user, field, None))  # 值未变化检查
            )
        }

        # 生成最终更新数据
        update_data = {k: v for k, v in update_data.items() if k not in excluded_fields}

        if "password" in update_data:
            update_data["password"] = make_password(update_data["password"])
        print(update_data)
        serializer = FrontendUserSerializer(
            instance=user, data=update_data, partial=True
        )
        if not serializer.is_valid():
            return Response({"errors": serializer.errors}, status=400)
        serializer.save()
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
    except jwt.ExpiredSignatureError:
        return Response({"error": "Token 已过期"}, status=status.HTTP_401_UNAUTHORIZED)
    except jwt.InvalidTokenError:
        return Response({"error": "Token 无效"}, status=status.HTTP_401_UNAUTHORIZED)
    except FrontendUser.DoesNotExist:
        return Response({"error": "用户不存在"}, status=status.HTTP_404_NOT_FOUND)

    # serializer = FrontendUserSerializer(data=data)
    # if not serializer.is_valid():
    #     return Response(
    #         {"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
    #     )
    # 处理密码更新
    # if "password" in request.data:
    #     user.set_password(request.data["password"])

    # 处理头像更新
    # if avatar_file:
    #     user.avatar.save(avatar_file.name, avatar_file)

    # serializer.save()

    # return Response(
    #     {
    #         "user": FrontendUserSerializer(user).data,
    #         "new_access_token": generate_tokens(user)[0],  # 可选返回新token
    #     }
    # )

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


@api_view(["GET"])
def get_exams(request):
    """ 获取指定类别的所有试题（单题 & 题组）并保证 ID 递增唯一 """

    # 获取前端传入的类别参数
    category_name = request.query_params.get("category")
    if not category_name:
        return Response({"error": "缺少 category 参数"}, status=400)

    # 查询类别对象
    try:
        category = Category.objects.get(name=category_name)
    except Category.DoesNotExist:
        return Response({"error": "该类别不存在"}, status=404)

    # 获取所有属于该类别的独立试题
    standalone_problems = Problem.objects.filter(categories=category, exam_set__isnull=True).order_by("id")

    # 获取所有属于该类别的试题组
    exam_sets = ExamSet.objects.prefetch_related(
        Prefetch("problems", queryset=Problem.objects.order_by("question_number"))
    ).filter(categories=category).order_by("id")

    # 统一编号（确保 ID 递增）
    all_questions = []
    id_counter = 1  # 递增 ID

    # 处理独立试题
    for problem in standalone_problems:
        serialized_problem = ProblemSerializer(problem).data
        serialized_problem["id"] = str(id_counter)  # 赋值递增 ID
        all_questions.append(serialized_problem)
        id_counter += 1  # 递增 ID

    # 处理题组及其小题
    for exam in exam_sets:
        exam_data = ExamSetSerializer(exam).data
        exam_id = str(id_counter)  # 记录大题 ID
        exam_data["id"] = exam_id  # 题组 ID
        exam_data["sub_questions"] = []

        for index, problem in enumerate(exam_data["problems"], start=1):
            problem["id"] = f"{exam_id}-{index}"  # 采用 "大题ID-小题编号" 格式
            exam_data["sub_questions"].append(problem)

        # 移除原 `problems`，换成 `sub_questions`
        del exam_data["problems"]
        all_questions.append(exam_data)
        id_counter += 1  # 递增大题 ID

    # 返回 JSON 数据
    return Response(all_questions)