import uuid
from django.contrib.auth.hashers import make_password, check_password
from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _


def user_avatar_path(instance, filename):
    """定义头像的存储路径，按 user_id 存储"""
    return f'avatars/{instance.user_id}/{filename}'

# 前端用户模型
class FrontendUser(models.Model):
    # 用户唯一ID
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # 用户信息
    username = models.CharField(max_length=100, unique=True)  # 用户名
    password = models.CharField(max_length=255)  # 加密存储密码
    email = models.EmailField(unique=True)  # 邮箱
    avatar = models.ImageField(upload_to=user_avatar_path, null=True, blank=True)  # 头像存储路径

    # 可选信息
    GENDER_CHOICES = [
        ('M', '男'),
        ('F', '女'),
        ('O', '其他'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)  # 性别

    GRADE_CHOICES = [
        ('G1', '高一'),
        ('G2', '高二'),
        ('G3', '高三'),
    ]
    grade = models.CharField(max_length=2, choices=GRADE_CHOICES, blank=True, null=True)  # 年级

    remarks = models.TextField(blank=True, null=True)  # 备注
    correct_problems = models.IntegerField(default=0)  # 正确题目数

    # 系统信息
    created_at = models.DateTimeField(auto_now_add=True)  # 用户注册时间

    def set_password(self, raw_password):
        """加密存储用户密码"""
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        """验证用户密码"""
        return check_password(raw_password, self.password)

    def __str__(self):
        return f"{self.username} ({self.user_id})"

# 试题分类表（年份、地区、考点）
class Category(models.Model):
    CATEGORY_TYPES = [("year", "年份"), ("region", "地区"), ("topic", "考点")]

    name = models.CharField(max_length=100, unique=True)  # 类别名称
    category_type = models.CharField(max_length=20, choices=CATEGORY_TYPES)  # 具体分类类型

    def __str__(self):
        return f"{self.name} ({self.get_category_type_display()})"

# 试题组（大题）
class ExamSet(models.Model):
    title = models.TextField()  # 试题组标题
    description = models.TextField()  # 试题材料、背景信息
    image = models.ImageField(upload_to="examsets/", null=True, blank=True)  # 相关图片（可选）
    categories = models.ManyToManyField(Category)  # 关联分类（可多个）
    created_at = models.DateTimeField(auto_now_add=True)  # 试题创建时间

    def __str__(self):
        return self.title

# 试题表（支持单题和子题）
class Problem(models.Model):
    QUESTION_TYPES = [
        ("single", "单选"),
        ("multiple", "多选"),
    ]

    categories = models.ManyToManyField(Category)  # 关联分类（适用于单题）
    exam_set = models.ForeignKey(ExamSet, on_delete=models.CASCADE, related_name="problems", null=True, blank=True)  # 关联试题组
    question_number = models.PositiveIntegerField(null=True, blank=True)  # 小题编号（如 "1"、"2"（仅子题使用））
    question = models.TextField()  # 小题题干
    type = models.CharField(max_length=10, choices=QUESTION_TYPES, default="single")  # 题型
    choices = models.JSONField()  # 选择题选项（A/B/C/D）
    answer = models.JSONField()  # 正确答案（支持单选 & 多选）
    explanation = models.TextField()  # 解析
    created_at = models.DateTimeField(auto_now_add=True)  # 题目创建时间

    def __str__(self):
        if self.exam_set:
            return f"题组 {self.exam_set.id} - 小题 {self.question_number}"
        return f"独立试题: {self.question[:30]}"  # 单题时显示前30个字符

# 用户错题表
class UserHistory(models.Model):
    frontend_user = models.ForeignKey(FrontendUser, on_delete=models.CASCADE)  # 关联前端用户
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)  # 关联错题
    user_answer = models.CharField(max_length=10)  # 用户作答答案
    attempt_time = models.DateTimeField(auto_now_add=True)  # 记录答题时间
    is_correct = models.BooleanField(default=False)  # 是否答对

    def __str__(self):
        return f"{self.frontend_user.username} 的错题记录 - 题目 {self.problem.id}"


# 用户对话记录表
class UserConversation(models.Model):
    frontend_user = models.ForeignKey(FrontendUser, on_delete=models.CASCADE)  # 用户
    precursor_id = models.CharField(max_length=100, unique=True, blank=True,null=True )  # 前向会话ID
    session_id = models.CharField(max_length=100, unique=True)  # 独立会话ID
    timestamp = models.DateTimeField(auto_now_add=True)  # 记录时间
    user_message = models.TextField()  # 用户输入
    llm_response = models.TextField()  # LLM 回复

    def __str__(self):
        return f"{self.frontend_user.username} 会话 {self.session_id} - {self.timestamp}"

# 调用外部 API 所需的 Key 表
class APIConfig(models.Model):

    SERVICE_CHOICES = [
        ('openai', 'OpenAI API'),
        ('google', 'Google API'),
        ('baidu', 'Baidu API'),
        ('deepseek', 'DeepSeek API'),
        ('xfyun', '讯飞星火 API'),
        ('custom', '自定义 API'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # 唯一 ID
    service_name = models.CharField(max_length=50, choices=SERVICE_CHOICES)  # API 服务名称
    api_key = models.CharField(max_length=200)  # API Key
    api_secret = models.CharField(max_length=200, blank=True, null=True)  # API Secret（部分 API 需要）
    app_id = models.CharField(max_length=100, blank=True, null=True)  # APPID

    host = models.CharField(max_length=200, blank=True, null=True)  # API 服务器地址（如 'spark-api.xf-yun.com'）
    path = models.CharField(max_length=200, blank=True, null=True)  # API 访问路径（如 '/v4.0/chat'）

    created_at = models.DateTimeField(default=now)  # Key 创建时间
    last_used_at = models.DateTimeField(blank=True, null=True)  # 上次使用时间
    usage_count = models.IntegerField(default=0)  # 使用次数
    is_active = models.BooleanField(default=True)  # 是否启用 Key

    extra_params = models.JSONField(blank=True, null=True)  # 额外参数（JSON 格式，可选）

    def __str__(self):
        return f"{self.get_service_name_display()} - {'启用' if self.is_active else '禁用'}"
