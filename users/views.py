from datetime import timedelta, datetime

import jwt
import requests
from django.utils.timezone import now

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response  # 使用 DRF 的 Response
from rest_framework.decorators import api_view, parser_classes, permission_classes
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth.hashers import make_password, check_password

from GeoVisionary_Backend import settings
from users.utils.MyJWT import generate_tokens, decode_token
from django.db.models import Prefetch
from .models import FrontendUser, Problem, ExamSet, Category, UserHistory, UserLearningBehavior, RecommendationContent, \
    UserRating, Video, TextContent, RecommendationScore, UserFavorite, Feedback
from .serializers import FrontendUserSerializer, ProblemSerializer, ExamSetSerializer, UserHistorySerializer, \
    UserLearningBehaviorSerializer, RecommendationContentSerializer, UserRatingSerializer, UserFavoriteSerializer, \
    FeatureVectorSerializer


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
    # 初始化学习行为记录
    user_learning = UserLearningBehavior.objects.create(user=user)
    user_learning.update_active_time()
    user_learning.update_last_learning_interval()

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
        # 更新学习行为数据
        user_learning = UserLearningBehavior.objects.get_or_create(user=user)[0]
        user_learning.update_active_time()
        user_learning.update_last_learning_interval()

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
        return Response({"error": "无效或过期的 refresh_token"}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        user = FrontendUser.objects.get(user_id=user_id)
        access_token, refresh_token = generate_tokens(user)
        return Response({"access_token": access_token, "refresh_token": refresh_token})
    except FrontendUser.DoesNotExist:
        return Response({"error": "用户不存在"}, status=status.HTTP_401_UNAUTHORIZED)


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
        # 更新用户学习行为
        user_learning = UserLearningBehavior.objects.get_or_create(user=user)[0]
        user_learning.update_active_time()  # 更新活跃时间
        user_learning.update_last_learning_interval()  # 更新最近学习时间间隔

        # 生成序列化信息
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
            return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
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
    # 用户历史和信息
    user_histories = UserHistory.objects.all()
    user_list = FrontendUser.objects.all()
    # 更新所有用户的正确题数
    histories_dict = {}
    # 遍历用户做题历史，统计用户正确题目数
    for item in user_histories:
        username = str(item).split('的错题记录')[0].strip()  # 获取用户名
        if username not in histories_dict:
            histories_dict[username] = 0
        if item.is_correct:
            histories_dict[username] += 1

    # 遍历用户，如果有记录就设为记录，否则为 0
    for user in user_list:
        if user.username not in histories_dict:
            user.correct_problems = 0
            user.save(update_fields=['correct_problems'])
        else:
            user.correct_problems = histories_dict[user.username]
            user.save(update_fields=['correct_problems'])

    response_dict = {}
    for obj in user_list:
        response_dict[obj.username] = {
            'correct_problems': obj.correct_problems,
            'avatar': request.build_absolute_uri(obj.avatar.url) if obj.avatar else None  # 生成完整URL
        }
    return Response({"user_object": response_dict},status=status.HTTP_200_OK)


@api_view(["GET"])
def get_exams(request):
    """ 获取指定类别的所有试题（单题 & 题组）并保证 ID 递增唯一 """

    # 获取前端传入的类别参数
    category_name = request.query_params.get("category")
    if not category_name:
        return Response({"error": "缺少 category 参数"}, status=status.HTTP_400_BAD_REQUEST)

    # 查询类别对象
    try:
        category = Category.objects.get(name=category_name)
    except Category.DoesNotExist:
        return Response({"error": "该类别不存在"}, status=status.HTTP_404_NOT_FOUND)

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

@api_view(['POST'])
def save_user_history(request):
    histories = request.data.get("history")
    print(histories)
    user = request.data.get("user")
    if not user:
        return Response({'message': '缺少用户信息，无法保存答题详情'}, status=status.HTTP_400_BAD_REQUEST)

    frontend_user = FrontendUser.objects.filter(user_id=user['user_id']).first()
    if not frontend_user:
        return Response({'message': '用户不存在'}, status=status.HTTP_404_NOT_FOUND)

    # 遍历所有的答题历史
    for index, history in histories.items():
        question = ''
        try:
            # 单题和多题分别处理
            if not "selected" in history:
                for sub_index, sub_history in history.items():
                    if "hasHistory" in sub_history and sub_history["hasHistory"]:
                        continue
                    question = sub_history["question"]
                    problem = Problem.objects.get(question=question)
                    UserHistory.objects.create(
                        frontend_user=frontend_user,
                        problem=problem,
                        user_answer=",".join(sub_history.get('selected', [])),
                        is_correct=sub_history.get('correct', False)
                    )
            else:
                if "hasHistory" in history and history["hasHistory"]:
                    continue  # 如果存在历史记录，则跳过保存
                question = history["question"]
                problem = Problem.objects.get(question=question)
                UserHistory.objects.create(
                    frontend_user=frontend_user,
                    problem=problem,
                    user_answer=",".join(history.get('selected', [])),
                    is_correct=history.get('correct', False)
                )

        except Problem.DoesNotExist:
            return Response({'message': f'题目 {question} 不存在'}, status=status.HTTP_404_NOT_FOUND)

    return Response({'message': '答题详情已保存'}, status=status.HTTP_200_OK)

@api_view(['POST'])
def load_user_history(request):
    user = request.data.get("user")
    if not user:
        return Response({'message': '缺少用户信息，无法加载答题详情'}, status=status.HTTP_400_BAD_REQUEST)

    frontend_user = FrontendUser.objects.filter(user_id=user['user_id']).first()
    if not frontend_user:
        return Response({'message': '用户不存在'}, status=status.HTTP_404_NOT_FOUND)

    histories = UserHistory.objects.filter(frontend_user=frontend_user)
    serializer = UserHistorySerializer(histories, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def log_user_activity(request):
    """记录用户的学习频率或点击行为"""
    try:
        data = request.data
        user_id = data.get("user_id")
        content_type = data.get("content_type")  # 只应是 video 或 text
        content_key = data.get("content_key") # bvid-p 或 keyword
        action = data.get("action")  # study 或 click

        # 查找用户和学习行为数据
        user = FrontendUser.objects.get(user_id=user_id)
        user_learning, _ = UserLearningBehavior.objects.get_or_create(user=user)

        if action == "study":
            user_learning.update_study_frequency()
        elif action == "click" and content_type and content_key:
            user_learning.update_content_click_rate(content_type)

            click_rec_content,_ = RecommendationContent.objects.get_or_create(
                content_type=content_type,
                content_key=content_key,
            )
            click_rec_content.update_clicks()
            click_rec_content.record_click()

        else:
            return Response({"error": "不合法的行为，或是错误的推荐内容类别"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "用户行为数据更新成功！"}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def log_user_rating(request):
    # 获取日志信息
    data = request.data
    user_id = data.get("user_id")
    content_type = data.get("content_type")
    rating_type = data.get("rating_type")
    ratings = data.get("rating") # 内存放包含 content_key 信息的数组

    user = FrontendUser.objects.get(user_id=user_id)
    if not user:
        return Response("用户不存在！", status=status.HTTP_404_NOT_FOUND)

    if rating_type == 'rating':
        for rating in ratings:
            assert isinstance(rating, dict)
            key = next(iter(rating))
            value = rating[key]
            rating_content = RecommendationContent.objects.filter(
                content_type=content_type, content_key=key
            ).first()

            if not rating_content:
                continue

            user_rating, created = UserRating.objects.get_or_create(
                user=user, content=rating_content
            )

            if value == 0:
                # 用户想要删除评分
                user_rating.delete()
            else:
                # 用户更新评分
                user_rating.rating = value
                user_rating.save()

    elif rating_type == 'favorite':
        # 获取用户数据库中已有的收藏内容
        current_favorites = set(
            UserFavorite.objects.filter(user=user, content__content_type=content_type)
            .values_list("content__content_key", flat=True)
        )

        # 计算前端传来的新收藏列表
        new_favorites = set(ratings)
        print(new_favorites)

        # 找到需要删除的（数据库有但前端没有）
        to_delete = current_favorites - new_favorites

        # 找到需要新增的（前端有但数据库没有）
        to_add = new_favorites - current_favorites

        # 批量删除
        UserFavorite.objects.filter(user=user, content__content_key__in=to_delete).delete()

        # 批量添加
        new_favorite_objects = [
            UserFavorite(user=user, content=RecommendationContent.objects.get(content_key=key))
            for key in to_add
        ]
        UserFavorite.objects.bulk_create(new_favorite_objects)

    else:
        return Response({"message": "未知评价类型！"}, status=status.HTTP_400_BAD_REQUEST)

    return Response({"message": "用户评价已更新！"},status=status.HTTP_200_OK)

@api_view(['POST'])
def get_user_rating(request):
    data = request.data
    user_id = data.get("user_id")
    content_type = data.get("content_type")
    rating_type = data.get("rating_type")
    data = []
    if not user_id:
        return Response({"message": "用户不存在！"},status=status.HTTP_400_BAD_REQUEST)

    if rating_type == 'rating':
        rated_contents = UserRating.objects.filter(content__content_type=content_type,user_id=user_id)
        for content in rated_contents:
            content_dict = {content.content.content_key:content.rating}
            data.append(content_dict)

    elif rating_type == 'favorite':
        favorite_contents = UserFavorite.objects.filter(content__content_type=content_type,user_id=user_id)
        for content in favorite_contents:
            data.append(content.content.content_key)

    else:
        return Response({"message": "未知评价类型"},status=status.HTTP_400_BAD_REQUEST)

    return Response({"data":data},status=status.HTTP_200_OK)

@api_view(['GET'])
def get_recommend_items(request):
    user_id = request.GET.get('user_id')
    recommend_type = request.GET.get('recommend_type')
    if recommend_type not in ['text', 'video']:
        return Response({"message":"未知推荐类型！"},status=status.HTTP_400_BAD_REQUEST)

    response_list = []
    # 如果没有用户 ID 或推荐分数表没有该用户，直接按照受欢迎度推荐，否则按照推荐分数从高到低推荐
    if not user_id or not RecommendationScore.objects.filter(user_id=user_id).exists():
        recommend_contents = RecommendationContent.objects.filter(content_type=recommend_type).order_by("-popularity", "-id")
    else:
        recommend_scores = RecommendationScore.objects.filter(user_id=user_id).select_related("content").order_by("-score", "-id")
        recommend_contents = [rec_score.content for rec_score in recommend_scores if rec_score.content.content_type == recommend_type]

    # 遍历列表，根据内容类型添加推荐内容
    for recommend_content in recommend_contents:
        if recommend_content.content_type == 'text':
            keyword = recommend_content.content_key
            response_list.append(keyword)
        elif recommend_content.content_type == 'video':
            bvid, p = recommend_content.content_key.split('-')
            response_list.append({"bvid": bvid, "p": p})

    return Response({"data":response_list},status=status.HTTP_200_OK)

@api_view(['GET'])
def send_feature_data(request):
    # 获取构建特征向量的特征值
    users = FrontendUser.objects.all()
    # users_histories = UserHistory.objects.all() 用户答题历史记录，需要特征工程
    users_favorites = UserFavorite.objects.all()
    users_ratings = UserRating.objects.all()
    users_learning_behavior = UserLearningBehavior.objects.all()
    rec_contents = RecommendationContent.objects.all()

    feature_data = []
    target_data = []
    # 将信息序列化成为 json 格式
    for user in users:
        # 用户基本信息
        user_id = user.user_id
        grade = user.grade
        gender = user.gender
        correct_problems = user.correct_problems

        # 用户学习行为
        user_learning_behavior = users_learning_behavior.filter(user_id=user_id).first()
        # 不存在时使用空值
        if not user_learning_behavior:
            learning_interval = ''
            study_frequency_last_7_days = {}
            active_time_distribution = {}
            content_click_rate = {}
            updated_at = now()
        else:
            learning_interval = user_learning_behavior.last_learning_time_interval
            study_frequency_last_7_days = user_learning_behavior.study_frequency_last_7_days
            active_time_distribution = user_learning_behavior.active_time_distribution
            content_click_rate = user_learning_behavior.content_click_rate
            updated_at = user_learning_behavior.updated_at

        # 推荐内容信息
        for rec_content in rec_contents:
            favorite_object = users_favorites.filter(content=rec_content,user_id=user_id).first()
            rating_object = users_ratings.filter(content=rec_content,user_id=user_id).first()
            # 无评价且无收藏，记录为 exposure （即未点击过）
            clicked = 1.0
            if not rating_object and not favorite_object:
                clicked = 0.0

            # 无评价时，评分设为 0，评价时间设为现在 （时间差为 0）
            if not rating_object:
                rating = 0
                rating_time = now()
            else:
                rating = rating_object.rating
                rating_time = rating_object.updated_at

            # 有收藏设为 True，否则 False
            if not favorite_object:
                favorite = False
            else:
                favorite = True

            # 存在记录，添加推荐内容基本信息
            content_type = rec_content.content_type
            content_key = rec_content.content_key
            total_clicks = rec_content.total_clicks
            created_at = rec_content.created_at

            # 构建特征向量并加入特征矩阵
            feature_vector = {
                "user_id":user_id,
                "grade":grade,
                "gender":gender,
                "correct_problems":correct_problems,
                "learning_interval":learning_interval,
                "study_frequency_last_7_days":study_frequency_last_7_days,
                "active_time_distribution":active_time_distribution,
                "content_click_rate":content_click_rate,
                "updated_at":updated_at,
                "content_type":content_type,
                "content_key":content_key,
                "total_clicks":total_clicks,
                "created_at":created_at,
                "rating":rating,
                "rating_time":rating_time,
                "favorite":favorite
            }
            target = {
                "click":clicked,
            }
            feature_data.append(feature_vector)
            target_data.append(target)
    # 辅助数据处理信息
    # need_one_hot = ["grade", "gender", "learning_interval", "content_type", "favorite"]
    need_normalize = ["correct_problems", "study_frequency_last_7_days", "total_clicks", "rating"]
    need_parse = ["study_frequency_last_7_days", "active_time_distribution", "content_click_rate"]
    need_label_encode = ["user_id", "content_key", "grade", "gender", "learning_interval", "content_type", "favorite"]
    need_process_datetime = {
        "created_at":['days'],
        "updated_at":['days', 'weekday'],
        "rating_time":['hours']
    }

    configs = {
        "sparse_fea_num": len(need_label_encode),
        "need_parse": need_parse,
        "need_normalize": need_normalize,
        # "need_one_hot": need_one_hot,
        "need_label_encode": need_label_encode,
        "need_process_datetime": need_process_datetime,
        "need_train": False
    }

    # 原始数据
    raw_data = {
        "inputs": FeatureVectorSerializer(feature_data, many=True).data,
        "targets": target_data,
        "configs": configs,
    }

    # 向模型端发送请求
    model_url = 'http://127.0.0.1:5000/recommend'
    response = requests.post(url=model_url, json=raw_data, headers={'Content-Type': 'application/json'})
    if response.status_code == status.HTTP_200_OK:
        response_data = response.json()
        recommendations = response_data['recommendations']
        for recommendation in recommendations:
            rec_content = RecommendationContent.objects.get(content_key=recommendation['content_key'], content_type=recommendation['content_type'])
            rec_object = RecommendationScore.objects.get_or_create(user_id=recommendation['user_id'], content=rec_content)[0]
            rec_object.score = recommendation['predict_score']
            rec_object.save(update_fields=['score'])
    else:
        return Response(status=response.status_code)

    return Response(response_data,status=status.HTTP_200_OK)

@api_view(['POST'])
def save_feedback(request):
    data = request.data
    user = data['user']
    content = data['content']
    user_object = FrontendUser.objects.get(user_id=user['user_id'])
    if not user_object:
        return Response("用户不存在！",status=status.HTTP_404_NOT_FOUND)

    Feedback.objects.create(
        user_id=user['user_id'],
        content=content,
    )

    return Response("反馈上传成功！",status=status.HTTP_201_CREATED)

@api_view(['POST'])
def get_learning_behavior(request):
    user = request.data.get('user')
    behavior_type = request.data.get('behavior_type')
    user_object = FrontendUser.objects.get(user_id=user['user_id'])
    if not user_object:
        return Response("用户不存在！",status=status.HTTP_404_NOT_FOUND)

    behavior_object = UserLearningBehavior.objects.get(user_id=user['user_id'])
    if not hasattr(behavior_object, behavior_type):
        return Response("用户行为不存在！",status=status.HTTP_404_NOT_FOUND)

    behavior_data = getattr(behavior_object, behavior_type)
    if behavior_type == 'study_frequency_last_7_days':
        # 获取今天的日期
        today = datetime.today().date()

        # 生成近7天的日期列表（含今天）
        last_7_days = [(today - timedelta(days=i)).isoformat() for i in range(7)]
        last_7_days.reverse()  # 从旧到新排列

        # 过滤出最近7天的数据，并补全缺失日期
        processed_data = {
            date_str: behavior_data.get(date_str, 0)
            for date_str in last_7_days
        }
        behavior_data = processed_data

    return Response(behavior_data,status=status.HTTP_200_OK)

@api_view(['POST'])
def get_favorites(request):
    data = request.data
    user = data['user']
    user_object = FrontendUser.objects.get(user_id=user['user_id'])
    if not user_object:
        return Response("用户不存在！",status=status.HTTP_404_NOT_FOUND)

    favorite_objects = UserFavorite.objects.filter(user_id=user['user_id'])
    if not favorite_objects:
        return Response("用户没有收藏任何内容！",status=status.HTTP_404_NOT_FOUND)

    favorite_content = []
    for obj in favorite_objects:
        favorite_content.append(str(obj.content))
    print(favorite_content)
    return Response(favorite_content,status=status.HTTP_200_OK)

@api_view(['GET','POST'])
def test_front_back_connection(request):
    if request.method == 'POST':
        data = request.data
        user_id = data.get("user_id")
        content_type = data.get("content_type")
        rating_type = data.get("rating_type")
        rating = data.get("rating")
        print(f"你请求了{user_id},{content_type},{rating_type},{rating}的数据！")
        return Response({'data':{'content_type':content_type,
                                 "rating_type":rating_type,"rating":rating}},status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_202_ACCEPTED)