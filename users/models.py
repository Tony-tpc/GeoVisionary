import uuid
from datetime import timedelta

from django.contrib.auth.hashers import make_password, check_password
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone
from django.utils.timezone import now


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

# 视频信息表
class Video(models.Model):
    bvid = models.CharField(max_length=20)
    p = models.IntegerField(default=1)  # 分P
    title = models.CharField(max_length=255)
    tags = models.JSONField(default=list, null=True, blank=True)  # 存储标签
    topic = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={"category_type": "topic"}
    )  # 关联考点
    cover_url = models.URLField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"视频{self.title}的bvid: {self.bvid}，p: {self.p}"

# 图文信息表
class TextContent(models.Model):
    keyword = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    topic = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={"category_type": "topic"}
    )  # 关联考点

    def __str__(self):
        return self.keyword

# 推荐内容分类表
class RecommendationContent(models.Model):
    content_type = models.CharField(max_length=10, choices=[('video', '视频'), ('text', '图文')])
    content_key = models.CharField(max_length=255)  # 视频的 bvid-p 或图文的 keyword
    p = models.PositiveIntegerField(null=True, blank=True)  # 分P编号，仅在收藏视频时使用
    category = models.ForeignKey(Category, on_delete=models.CASCADE, limit_choices_to={'category_type': 'topic'})  # 关联考点分类
    popularity = models.FloatField(default=0.0) # 受欢迎度，计算公式可以是点击率 × 0.3 + 收藏率 × 0.7
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.content_type == "video" and self.p is not None:
            bvid = self.content_key.split('-')[0]  # 只取 bvid 部分
            self.content_key = f"{bvid}-{self.p}"  # 生成唯一标识
        super().save(*args, **kwargs)

    def get_related_content(self):
        """
        根据 content_type 和 content_key 查询对应的视频或图文
        """
        if self.content_type == 'video':
            try:
                bvid, p = self.content_key.split('-')
                p = int(p)
                return Video.objects.get(bvid=bvid, p=p)
            except (ValueError, Video.DoesNotExist):
                return None
        elif self.content_type == 'text':
            return TextContent.objects.filter(keyword=self.content_key).first()
        return None

    def __str__(self):
        return f"{self.get_content_type_display()} - {self.content_key} ({self.category})"

# 推荐内容评分表
class RecommendationScore(models.Model):
    user = models.ForeignKey(FrontendUser, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, limit_choices_to={'category_type': 'topic'})
    score = models.FloatField(default=0.0)  # 推荐分数

    class Meta:
        unique_together = ('user', 'category')  # 保证同一用户对同一考点只有一个分数

    def __str__(self):
        return f"{self.user.username} - {self.category.name} - Score: {self.score}"

# 用户收藏表
class UserFavorite(models.Model):
    user = models.ForeignKey(FrontendUser, on_delete=models.CASCADE)
    content_type = models.CharField(max_length=10, choices=[('video', '视频'), ('text', '图文')])
    content_key = models.CharField(max_length=255)  # 存 bvid-p 或 keyword
    p = models.PositiveIntegerField(null=True, blank=True)  # 分P编号，仅在收藏视频时使用
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.content_type == 'video':
            return f"视频: {self.content_key} 收藏者: {self.user.username}"
        return f"{self.get_content_type_display()}: {self.content_key} 收藏者: {self.user.username}"

    def save(self, *args, **kwargs):
        if self.content_type == "video" and self.p is not None:
            bvid = self.content_key.split('-')[0]  # 只取 bvid 部分
            self.content_key = f"{bvid}-{self.p}"  # 生成唯一标识
        super().save(*args, **kwargs)

def default_active_time_counts():
    return {"morning": 0, "afternoon": 0, "evening": 0}

# 用户学习行为数据表
class UserLearningBehavior(models.Model):
    user = models.ForeignKey(FrontendUser, on_delete=models.CASCADE)

    # 过去7天的学习频率（存储为 JSON，如 {"2025-03-15": 3, "2025-03-16": 2, ...}）
    study_frequency_last_7_days = models.JSONField(default=dict)

    # 用户在特定知识点上的掌握度（如 {"地球自转": 0.8, "大气环流": 0.6}）
    topic_proficiency = models.JSONField(default=dict)

    # 用户活跃时间段（早上/中午/晚上）计数
    active_time_counts = models.JSONField(default=default_active_time_counts)

    # 用户活跃时间段（如 {"morning": 0.3, "afternoon": 0.5, "evening": 0.2}，值为占比）
    active_time_distribution = models.JSONField(default=dict)

    # 最近一次学习时间距离当前时间的间隔（1小时内、1天内、1周内等）
    LAST_LEARNING_CHOICES = [
        ("0","刚刚"),
        ("1h", "1小时内"),
        ("1d", "1天内"),
        ("1w", "1周内"),
        ("1m", "1月内"),
        ("long", "1个月以上"),
    ]
    last_learning_time_interval = models.CharField(max_length=5, choices=LAST_LEARNING_CHOICES, default="long")

    # 用户对不同类型内容的历史点击次数（如 {"video": 7, "text": 3}）
    content_click_count = models.JSONField(default=dict)

    # 用户对不同类型内容的历史点击率（如 {"video": 0.7, "text": 0.3}）
    content_click_rate = models.JSONField(default=dict)

    # 记录更新时间
    updated_at = models.DateTimeField(auto_now=True)

    def update_last_learning_interval(self):
        """更新最近学习时间的间隔"""
        last_learning = self.updated_at
        time_diff = timezone.localtime(timezone.now()) - last_learning

        if time_diff <= timedelta(minutes=1):
            self.last_learning_time_interval = "0"
        elif time_diff <= timedelta(hours=1):
            self.last_learning_time_interval = "1h"
        elif time_diff <= timedelta(days=1):
            self.last_learning_time_interval = "1d"
        elif time_diff <= timedelta(weeks=1):
            self.last_learning_time_interval = "1w"
        elif time_diff <= timedelta(weeks=4):
            self.last_learning_time_interval = "1m"
        else:
            self.last_learning_time_interval = "long"

        self.save(update_fields=["last_learning_time_interval"])

    def update_active_time(self):
        """更新用户活跃时间计数"""
        hour = timezone.localtime(timezone.now()).hour
        if 6 <= hour < 12:
            self.active_time_counts["morning"] += 1
        elif 12 <= hour < 18:
            self.active_time_counts["afternoon"] += 1
        else:
            self.active_time_counts["evening"] += 1

        total = sum(self.active_time_counts.values())
        if total > 0:
            self.active_time_distribution = {k: round(v / total, 3) for k, v in self.active_time_counts.items()}

        self.save()

    def __str__(self):
        return f"{self.user.username} 的学习行为数据"

    def update_study_frequency(self):
        """更新过去 7 天的学习频率"""
        today = now().date().isoformat()  # 获取当前日期的字符串格式（如 "2025-03-20"）
        print(today)

        # 更新今天的学习次数
        self.study_frequency_last_7_days[today] = self.study_frequency_last_7_days.get(today, 0) + 1

        # 只保留最近 7 天的数据
        seven_days_ago = now().date() - timedelta(days=7)
        self.study_frequency_last_7_days = {
            date: count for date, count in self.study_frequency_last_7_days.items()
            if date >= seven_days_ago.isoformat()
        }

        self.save(update_fields=["study_frequency_last_7_days"])

    def update_content_click_rate(self, content_type):
        """更新用户对不同类型内容的点击数据"""
        # 更新点击次数
        if content_type not in self.content_click_count:
            self.content_click_count[content_type] = 0
        self.content_click_count[content_type] += 1

        # 计算总点击量
        total_clicks = sum(self.content_click_count.values())

        # 计算并更新点击率
        if total_clicks > 0:
            self.content_click_rate = {
                k: round(v / total_clicks, 3) for k, v in self.content_click_count.items()
            }

        # 保存更新
        self.save(update_fields=["content_click_count", "content_click_rate"])