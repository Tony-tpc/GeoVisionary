from rest_framework import serializers
from .models import FrontendUser, ExamSet, Problem, Category, UserHistory, UserLearningBehavior, RecommendationContent, \
    UserRating, UserFavorite


class FrontendUserSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(required=False)  # 头像字段为可选项

    class Meta:
        model = FrontendUser
        fields = ["user_id", "username", "email", "password", "gender","grade","remarks","correct_problems","avatar","created_at"]
        extra_kwargs = {"password": {"write_only": True,"required":True}}  # 密码不能被读取

# 分类序列化器（返回 ID 和名称）
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "category_type"]


# 试题序列化器（适用于独立试题和子题）
class ProblemSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)  # 适用于独立试题
    answer = serializers.SerializerMethodField()  # 兼容单选和多选
    exam_set = serializers.PrimaryKeyRelatedField(queryset=ExamSet.objects.all(), allow_null=True, required=False)  # 允许为空（独立题目）

    class Meta:
        model = Problem
        fields = ["id", "question_number", "question", "type", "choices", "answer", "explanation", "exam_set", "categories"]

    def get_answer(self, obj):
        """确保返回的数据格式和前端一致"""
        if isinstance(obj.answer, dict) and "answer" in obj.answer:
            return obj.answer["answer"]  # 处理 JSONField 存储的答案
        return obj.answer  # 直接返回正确答案


# 试题组（大题）序列化器
class ExamSetSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)  # 题组的分类信息
    problems = ProblemSerializer(many=True, read_only=True)  # 题组的所有子题

    class Meta:
        model = ExamSet
        fields = ["id", "title", "description", "image", "categories", "problems"]

# 用户做题历史序列化器
class UserHistorySerializer(serializers.ModelSerializer):
    problem = ProblemSerializer(read_only=True)

    class Meta:
        model = UserHistory
        fields = ["problem", "user_answer", "is_correct"]
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        # 删除不必要的 frontend_user 信息
        data.pop('frontend_user', None)
        return data

# 推荐内容序列化器
class RecommendationContentSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = RecommendationContent
        fields = ["content_type", "content_key", "p", "category", "popularity", "created_at"]

# 用户评分序列化器
class UserRatingSerializer(serializers.ModelSerializer):
    user = FrontendUserSerializer(read_only=True)
    content = RecommendationContentSerializer(read_only=True)

    class Meta:
        model = UserRating
        fields = ["user", "content", "rating", "created_at", "updated_at"]

# 用户收藏序列化器
class UserFavoriteSerializer(serializers.ModelSerializer):
    user = FrontendUserSerializer(read_only=True)

    class Meta:
        model = UserFavorite
        fields = ["user", "content", "created_at"]

# 用户学习行为序列化器
class UserLearningBehaviorSerializer(serializers.ModelSerializer):
    user = FrontendUserSerializer(read_only=True)

    class Meta:
        model = UserLearningBehavior
        fields = ["user", "last_learning_time_interval", "study_frequency_last_7_days",
                  "topic_proficiency", "active_time_distribution", "content_click_rate", "updated_at"]

# 特征向量序列化器
class FeatureVectorSerializer(serializers.Serializer):
    user_id = serializers.UUIDField()
    grade = serializers.CharField()
    gender = serializers.CharField()
    correct_problems = serializers.IntegerField()
    questions_id = serializers.IntegerField(required=False)
    questions_category = serializers.CharField(required=False)
    question_type = serializers.CharField(required=False)
    is_correct = serializers.BooleanField(required=False)
    learning_interval = serializers.CharField()
    study_frequency_last_7_days = serializers.JSONField()
    active_time_distribution = serializers.JSONField()
    content_click_rate = serializers.JSONField()
    updated_at = serializers.DateTimeField()
    content_type = serializers.CharField()
    content_key = serializers.CharField()
    rating = serializers.IntegerField()
    total_clicks = serializers.IntegerField()
    created_at = serializers.DateTimeField()
    rating_time = serializers.DateTimeField()
    favorite = serializers.BooleanField()