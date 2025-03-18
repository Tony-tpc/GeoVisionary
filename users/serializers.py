from rest_framework import serializers
from .models import FrontendUser, ExamSet, Problem, Category

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