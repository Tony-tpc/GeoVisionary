from django.contrib import admin, messages
from django.utils.html import format_html
from django.utils.timezone import now
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import FrontendUser, Category, ExamSet, Problem, UserHistory, UserConversation, APIConfig, Video, \
    TextContent, RecommendationContent, RecommendationScore, UserLearningBehavior, UserRating, UserFavorite


# 用户管理
class FrontendUserAdmin(admin.ModelAdmin):
    list_display = ['get_user_id','get_username','get_email','get_gender','get_grade','get_remarks','get_correct_problems','get_avatar','get_created_at']
    list_per_page = 15
    list_filter = ['gender','grade','created_at']
    search_fields = ['user_id','username','email']

    # 显示、汉化、允许排序
    def get_user_id(self,obj:FrontendUser):
        return obj.user_id
    get_user_id.short_description = '用户ID'
    get_user_id.admin_order_field = 'user_id'

    def get_username(self,obj:FrontendUser):
        return obj.username
    get_username.short_description = '用户名'
    get_username.admin_order_field = 'username'

    def get_email(self,obj:FrontendUser):
        return obj.email
    get_email.short_description = '邮箱'
    get_email.admin_order_field = 'email'

    def get_gender(self,obj:FrontendUser):
        return obj.gender
    get_gender.short_description = '性别'
    get_gender.admin_order_field = 'gender'

    def get_grade(self,obj:FrontendUser):
        return obj.grade
    get_grade.short_description = '年级'
    get_grade.admin_order_field = 'grade'

    def get_remarks(self,obj:FrontendUser):
        return obj.remarks
    get_remarks.short_description = '个人签名'

    def get_correct_problems(self,obj:FrontendUser):
        return obj.correct_problems
    get_correct_problems.short_description = '正确题目数'
    get_correct_problems.admin_order_field = 'correct_problems'

    def get_avatar(self,obj:FrontendUser):
        return obj.avatar
    get_avatar.short_description = '头像'

    def get_created_at(self,obj:FrontendUser):
        return obj.created_at
    get_created_at.short_description = '注册时间'
    get_created_at.admin_order_field = 'created_at'

    def changelist_view(self, request, extra_context=None):
        # 当访问管理界面时，更新所有用户的正确题数
        user_histories = UserHistory.objects.all()
        histories_dict = {}
        # 遍历用户做题历史，统计用户正确题目数
        for item in user_histories:
            username = str(item).split('的错题记录')[0].strip() # 获取用户名
            if username not in histories_dict:
                histories_dict[username] = 0
            if item.is_correct:
                histories_dict[username] += 1
        users = FrontendUser.objects.all()
        # 遍历用户，如果有记录就设为记录，否则为 0
        for user in users:
            if user.username not in histories_dict:
                user.correct_problems = 0
                user.save(update_fields=['correct_problems'])
            else:
                user.correct_problems = histories_dict[user.username]
                user.save(update_fields=['correct_problems'])

        # 调用原有的 changelist_view 以保持正常的管理界面功能
        return super().changelist_view(request, extra_context)

admin.site.register(FrontendUser,FrontendUserAdmin)

# 分类管理
class CategoryAdmin(ImportExportModelAdmin):
    list_display = ['get_name','get_category_type']
    list_per_page = 10
    list_filter = ['category_type']
    search_fields = ['name','category_type']

    # 显示、汉化、允许排序
    def get_category_type(self, obj: Category):
        return obj.category_type
    get_category_type.short_description = '类别'
    get_category_type.admin_order_field = 'category_type'

    def get_name(self, obj: Category):
        return obj.name
    get_name.short_description = '名称'
    get_name.admin_order_field = 'name'

    # 自定义导入导出行为
    class ProxyResource(resources.ModelResource):
        class Meta:
            model = Category
    resource_class = ProxyResource

admin.site.register(Category,CategoryAdmin)

# 试题组管理
class ExamSetAdmin(ImportExportModelAdmin):
    list_display = ['id','get_title','get_description','get_image_preview','get_categories','get_created_at']
    list_per_page = 10
    list_filter = ['categories','created_at']
    search_fields = ['title','description','categories__name']

    # 显示、汉化、允许排序
    def get_categories(self, obj: ExamSet):
        return ", ".join([category.name for category in obj.categories.all()])
    get_categories.short_description = '类别'
    get_categories.admin_order_field = 'categories'

    def get_title(self, obj: ExamSet):
        return obj.title
    get_title.short_description = '标题'
    get_title.admin_order_field = 'title'

    def get_description(self, obj: ExamSet):
        return obj.description
    get_description.short_description = '试题背景'

    def get_image_preview(self, obj: ExamSet):
        if obj.image:
            return format_html('<img src="{}" width="100px" height="auto"/>', obj.image.url)
        return "无图片"
    get_image_preview.short_description = '图片预览'

    def get_created_at(self, obj: ExamSet):
        return obj.created_at
    get_created_at.short_description = '建立时间'
    get_created_at.admin_order_field = 'created_at'

    class ProxyResource(resources.ModelResource):
        class Meta:
            model = ExamSet
    resource_class = ProxyResource

admin.site.register(ExamSet,ExamSetAdmin)

# 试题表管理
class ProblemAdmin(ImportExportModelAdmin):
    list_display = ['id','get_exam_set','get_question_number','get_question','get_choices_formatted','get_answer','get_explanation','get_categories','get_created_at']
    list_per_page = 10
    list_filter = ['created_at','categories']
    search_fields = ['question','categories__name','exam_set__title']

    # 显示、汉化、允许排序
    def get_exam_set(self, obj: Problem):
        return obj.exam_set
    get_exam_set.short_description = '试题组'
    get_exam_set.admin_order_field = 'exam_set'

    def get_question_number(self, obj: Problem):
        return obj.question_number
    get_question_number.short_description = '小题编号'
    get_question_number.admin_order_field = 'question_number'

    def get_question(self, obj: Problem):
        return obj.question
    get_question.short_description = '小题题干'
    get_question.admin_order_field = 'question'

    def get_choices_formatted(self, obj: Problem):
        """ 美化选项显示（换行） """
        return format_html("<br>".join([f"<b>{key}</b>: {value}" for key, value in obj.choices.items()]))
    get_choices_formatted.short_description = '选项'

    def get_answer(self, obj: Problem):
        """ 获取答案唯一值，并用逗号隔开 """
        value = next(iter(obj.answer.values()))
        return format_html(",".join([f"<b>{item}</b>" for item in value]))
    get_answer.short_description = '答案'
    get_answer.admin_order_field = 'answer'

    def get_explanation(self, obj: Problem):
        return obj.explanation
    get_explanation.short_description = '解析'

    def get_categories(self, obj: Problem):
        return ", ".join([category.name for category in obj.categories.all()])
    get_categories.short_description = '类别'
    get_categories.admin_order_field = 'categories'

    def get_created_at(self, obj: Problem):
        return obj.created_at
    get_created_at.short_description = '建立时间'
    get_created_at.admin_order_field = 'created_at'

    # 导入/导出配置
    class ProxyResource(resources.ModelResource):
        class Meta:
            model = Problem
    resource_class = ProxyResource

admin.site.register(Problem,ProblemAdmin)

# 用户历史记录管理
class UserHistoryAdmin(admin.ModelAdmin):
    # 指定展示内容
    list_display = ['get_frontend_user', 'get_problem', 'get_user_answer', 'get_attempt_time', 'get_is_correct']

    # 指定一页显示多少条数据
    list_per_page = 10

    # 过滤器
    list_filter = ['is_correct']

    # 搜索框
    search_fields = ['frontend_user__username', 'problem__question', 'user_answer']

    # 按做题时间降序排序
    ordering = ('-attempt_time',)

    # 显示、汉化、允许排序
    def get_frontend_user(self, obj: UserHistory):
        return obj.frontend_user
    get_frontend_user.short_description = '用户'
    get_frontend_user.admin_order_field = 'frontend_user'

    def get_problem(self, obj: UserHistory):
        return obj.problem
    get_problem.short_description = '题目'
    get_problem.admin_order_field = 'problem'

    def get_user_answer(self, obj: UserHistory):
        return obj.user_answer
    get_user_answer.short_description = '用户答案'
    get_user_answer.admin_order_field = 'user_answer'

    def get_attempt_time(self, obj: UserHistory):
        return obj.attempt_time
    get_attempt_time.short_description = '作答时间'
    get_attempt_time.admin_order_field = 'attempt_time'

    def get_is_correct(self, obj: UserHistory):
        return obj.is_correct
    get_is_correct.short_description = '是否正确'
    get_is_correct.admin_order_field = 'is_correct'

admin.site.register(UserHistory, UserHistoryAdmin)

class UserConversationAdmin(admin.ModelAdmin):
    list_display = ['get_frontend_user','get_precursor_id','get_session_id','get_timestamp','get_user_message','get_llm_response']
    list_per_page = 10
    search_fields = ['frontend_user__username','session_id','timestamp']

    # 显示、汉化、允许排序
    def get_frontend_user(self, obj: UserConversation):
        return obj.frontend_user
    get_frontend_user.short_description = '用户'
    get_frontend_user.admin_order_field = 'frontend_user'

    def get_precursor_id(self, obj: UserConversation):
        return obj.precursor_id
    get_precursor_id.short_description = '前驱ID'
    get_precursor_id.admin_order_field = 'precursor_id'

    def get_session_id(self, obj: UserConversation):
        return obj.session_id
    get_session_id.short_description = '会话ID'
    get_session_id.admin_order_field = 'session_id'

    def get_timestamp(self, obj: UserConversation):
        return obj.timestamp
    get_timestamp.short_description = '时间戳'
    get_timestamp.admin_order_field = 'timestamp'

    def get_user_message(self, obj: UserConversation):
        return obj.user_message
    get_user_message.short_description = '用户输入'

    def get_llm_response(self, obj: UserConversation):
        return obj.llm_response
    get_llm_response.short_description = 'llm输出'

admin.site.register(UserConversation,UserConversationAdmin)

class APIConfigAdmin(admin.ModelAdmin):
    list_display = ['get_service_name','get_api_key','get_api_secret','get_app_id','get_host','get_path','get_created_at','get_last_used_at','get_usage_count','get_is_active']
    list_per_page = 10
    list_filter = ['service_name','is_active']
    search_fields = ['api_key','app_id','host','path','created_at','last_used_at','usage_count']

    # 显示、汉化、允许排序
    def get_service_name(self, obj: APIConfig):
        return obj.service_name
    get_service_name.short_description = 'API 服务名称'
    get_service_name.admin_order_field = 'service_name'

    def get_api_key(self, obj: APIConfig):
        return obj.api_key
    get_api_key.short_description = 'API Key'
    get_api_key.admin_order_field = 'api_key'

    def get_api_secret(self, obj: APIConfig):
        return obj.api_secret
    get_api_secret.short_description = 'API 密码'

    def get_app_id(self, obj: APIConfig):
        return obj.app_id
    get_app_id.short_description = 'App ID'

    def get_host(self, obj: APIConfig):
        return obj.host
    get_host.short_description = '服务器地址'

    def get_path(self, obj: APIConfig):
        return obj.path
    get_path.short_description = '访问路径'

    def get_created_at(self, obj: APIConfig):
        return obj.created_at
    get_created_at.short_description = '建立时间'
    get_created_at.admin_order_field = 'created_at'

    def get_last_used_at(self, obj: APIConfig):
        return obj.last_used_at
    get_last_used_at.short_description = '上次使用时间'
    get_last_used_at.admin_order_field = 'last_used_at'

    def get_usage_count(self, obj: APIConfig):
        return obj.usage_count
    get_usage_count.short_description = '使用次数'
    get_usage_count.admin_order_field = 'usage_count'

    def get_is_active(self, obj: APIConfig):
        return obj.is_active
    get_is_active.short_description = '是否启用'
    get_is_active.admin_order_field = 'is_active'

admin.site.register(APIConfig,APIConfigAdmin)

# 视频信息表管理
class VideoAdmin(ImportExportModelAdmin):
    list_display = ['get_bvid', 'get_p', 'get_title', 'get_tags', 'get_topic','get_cover_url', 'get_description', 'get_created_at', 'get_updated_at']
    list_per_page = 10
    list_filter = ['created_at', 'updated_at']
    search_fields = ['bvid', 'title', 'tags']

    def get_bvid(self, obj: Video):
        return obj.bvid
    get_bvid.short_description = '视频BVID'
    get_bvid.admin_order_field = 'bvid'

    def get_p(self, obj: Video):
        return obj.p
    get_p.short_description = '分P编号'
    get_p.admin_order_field = 'p'

    def get_title(self, obj: Video):
        return obj.title
    get_title.short_description = '视频标题'
    get_title.admin_order_field = 'title'

    def get_tags(self, obj: Video):
        tags_list = obj.tags if isinstance(obj.tags, list) else []
        return ", ".join(str(item) for item in tags_list) if tags_list else "无"
    get_tags.short_description = '标签'
    get_tags.admin_order_field = 'tags'

    def get_topic(self, obj: Video):
        return obj.topic
    get_topic.short_description = '考点'
    get_topic.admin_order_field = 'topic'

    def get_cover_url(self, obj: Video):
        return obj.cover_url if obj.cover_url else "无"
    get_cover_url.short_description = '封面链接'

    def get_description(self, obj: Video):
        return obj.description if obj.description else "无"
    get_description.short_description = '描述'

    def get_created_at(self, obj: Video):
        return obj.created_at
    get_created_at.short_description = '创建时间'
    get_created_at.admin_order_field = 'created_at'

    def get_updated_at(self, obj: Video):
        return obj.updated_at
    get_updated_at.short_description = '更新时间'
    get_updated_at.admin_order_field = 'updated_at'

    class ProxyResource(resources.ModelResource):
        class Meta:
            model = Video
    resource_class = ProxyResource

admin.site.register(Video, VideoAdmin)

# 图文信息表管理
class TextContentAdmin(ImportExportModelAdmin):
    list_display = ['get_keyword', 'get_description', 'get_topic']
    list_per_page = 10
    search_fields = ['keyword', 'description']

    def get_keyword(self, obj: TextContent):
        return obj.keyword
    get_keyword.short_description = '关键词'
    get_keyword.admin_order_field = 'keyword'

    def get_description(self, obj: TextContent):
        return obj.description
    get_description.short_description = '描述'

    def get_topic(self, obj: Video):
        return obj.topic
    get_topic.short_description = '考点'
    get_topic.admin_order_field = 'topic'

    class ProxyResource(resources.ModelResource):
        class Meta:
            model = TextContent
    resource_class = ProxyResource

admin.site.register(TextContent, TextContentAdmin)

# 推荐内容分类表管理
class RecommendationContentAdmin(ImportExportModelAdmin):
    list_display = ['get_content_type', 'get_content_key', 'get_category', 'get_popularity',
                    'get_total_clicks', 'get_weekly_clicks', 'get_created_at']
    list_per_page = 10
    list_filter = ['category', 'created_at']
    search_fields = ['content_key', 'category__name']
    actions = ['update_popularity_button']

    def get_content_type(self, obj: RecommendationContent):
        return obj.get_content_type_display()
    get_content_type.short_description = '内容类型'
    get_content_type.admin_order_field = 'content_type'

    def get_content_key(self, obj: RecommendationContent):
        return obj.content_key
    get_content_key.short_description = '内容ID'
    get_content_key.admin_order_field = 'content_key'

    def get_category(self, obj: RecommendationContent):
        return obj.category.name if obj.category else "暂无"
    get_category.short_description = '考点类别'
    get_category.admin_order_field = 'category__name'

    def get_created_at(self, obj: RecommendationContent):
        return obj.created_at
    get_created_at.short_description = '创建时间'
    get_created_at.admin_order_field = 'created_at'

    def get_popularity(self, obj: RecommendationContent):
        return round(obj.popularity, 5)
    get_popularity.short_description = '受欢迎度'
    get_popularity.admin_order_field = 'popularity'

    def get_total_clicks(self, obj: RecommendationContent):
        return obj.total_clicks
    get_total_clicks.short_description = '总点击数'
    get_total_clicks.admin_order_field = 'total_clicks'

    def get_weekly_clicks(self, obj: RecommendationContent):
        return format_html(",".join([f"<b>{key}</b>: {value}" for key, value in obj.weekly_clicks.items()]) if obj.weekly_clicks.items() else '暂无')
    get_weekly_clicks.short_description = '近 7 天点击数'

    def update_popularity_button(self, request, queryset=None):
        """管理员点击按钮后，更新所有推荐内容的受欢迎度"""
        self.update_popularity()
        self.message_user(request, "所有推荐内容的受欢迎度已成功更新！", level=messages.SUCCESS)

    update_popularity_button.short_description = "更新受欢迎度"
    update_popularity_button.type = 'success'
    update_popularity_button.icon = 'el-icon-star-off'

    def update_popularity(self):
        # 当访问管理界面时，更新所有推荐内容的受欢迎度（公式位于 markdown 中）
        m = 10 # 贝叶斯平滑系数
        decay_factor = 0.98 # 时间衰减系数 decay_factor
        click_weight = 0.2 # 点击权重 W_click
        fav_weight = 0.4 # 收藏权重 W_fav
        rating_weight = 0.4 # 评价权重 W_rating
        weekly_weight = 0.3 # 近 7 天评价权重 W_recent_rating

        updated_rec_contents = [] # 用于最后大更新数据库
        rec_contents = RecommendationContent.objects.all()
        # 计算全局好评率 p0（避免过低评分权重）
        global_avg_rating = UserRating.objects.filter(rating__gte=4).count() / max(UserRating.objects.count(), 1)
        for rec_content in rec_contents:
            rec_content.update_clicks() # 更新近 7 天点击数字典
            rec_content_favorite = UserFavorite.objects.filter(content=rec_content).count()
            rec_content_clicks = rec_content.total_clicks # total_clicks

            rec_content_ratings = UserRating.objects.filter(content=rec_content)
            rec_content_total_ratings = rec_content_ratings.count() # total_ratings
            rec_content_good_ratings = rec_content_ratings.filter(rating__gte=4).count() # good_ratings

            good_rating_ratio = (rec_content_good_ratings + m * global_avg_rating) / (rec_content_total_ratings + m)
            good_rating_weighted = good_rating_ratio * (rec_content_total_ratings + 1)  # 平衡权重

            # 综合考量点击数、收藏数、好评数
            popularity = (
                    click_weight * rec_content_clicks +
                    fav_weight * rec_content_favorite +
                    rating_weight * good_rating_weighted
            )

            # 时间衰减修正
            days_since_creation = (now().date() - rec_content.created_at.date()).days
            time_decay = decay_factor ** days_since_creation

            # 考虑时间衰减
            popularity = popularity * time_decay + weekly_weight * rec_content.weekly_clicks.get("total", 0)
            rec_content.popularity = popularity
            updated_rec_contents.append(rec_content)

        RecommendationContent.objects.bulk_update(updated_rec_contents, ['popularity'])

    class ProxyResource(resources.ModelResource):
        class Meta:
            model = RecommendationContent
    resource_class = ProxyResource

admin.site.register(RecommendationContent, RecommendationContentAdmin)

# 推荐分数表管理
class RecommendationScoreAdmin(ImportExportModelAdmin):
    list_display = ['get_user', 'get_content_key', 'get_score']
    list_per_page = 10
    list_filter = ['content__content_key']
    search_fields = ['user__username', 'content__content_key']
    ordering = ('user', '-score')  # 先按用户分组，再按分数降序

    def get_user(self, obj: RecommendationScore):
        return obj.user.username
    get_user.short_description = '用户名'
    get_user.admin_order_field = 'user__username'

    def get_content_key(self, obj: RecommendationScore):
        return obj.content.content_key
    get_content_key.short_description = '推荐内容'
    get_content_key.admin_order_field = 'content__content_key'

    def get_score(self, obj: RecommendationScore):
        return obj.score
    get_score.short_description = '推荐分数'
    get_score.admin_order_field = 'score'

    class ProxyResource(resources.ModelResource):
        class Meta:
            model = RecommendationScore
    resource_class = ProxyResource

admin.site.register(RecommendationScore, RecommendationScoreAdmin)

# 评分表资源类（用于导入/导出数据）
class UserRatingResource(resources.ModelResource):
    class Meta:
        model = UserRating

# 评分表管理
class UserRatingAdmin(ImportExportModelAdmin):
    list_display = ['get_user', 'get_content', 'get_rating', 'get_created_at', 'get_updated_at']
    list_per_page = 10
    list_filter = ['rating', 'content__content_key']
    search_fields = ['user__username', 'content__content_key']
    ordering = ['-updated_at']

    # 获取用户名
    def get_user(self, obj: UserRating):
        return obj.user.username
    get_user.short_description = '用户名'
    get_user.admin_order_field = 'user__username'

    # 获取推荐内容
    def get_content(self, obj: UserRating):
        return obj.content.content_key
    get_content.short_description = '推荐内容'
    get_content.admin_order_field = 'content__content_key'

    # 获取评分
    def get_rating(self, obj: UserRating):
        return obj.rating
    get_rating.short_description = '评分'
    get_rating.admin_order_field = 'rating'

    def get_created_at(self, obj: UserRating):
        return obj.created_at
    get_created_at.short_description = '评价时间'
    get_created_at.admin_order_field = 'created_at'

    def get_updated_at(self, obj: UserRating):
        return obj.updated_at
    get_updated_at.short_description = '更改时间'
    get_updated_at.admin_order_field = 'updated_at'

    resource_class = UserRatingResource  # 绑定数据导入导出功能

admin.site.register(UserRating, UserRatingAdmin)

# 用户收藏表管理
class UserFavoriteAdmin(ImportExportModelAdmin):
    list_display = ['get_user', 'get_content', 'get_created_at']
    list_per_page = 10
    list_filter = ['content__content_type', 'created_at']
    search_fields = ['user__username', 'content__content_key']

    def get_user(self, obj: UserFavorite):
        return obj.user.username
    get_user.short_description = '用户名'
    get_user.admin_order_field = 'user__username'

    def get_content(self, obj: UserFavorite):
        return obj.content.content_key
    get_content.short_description = '推荐内容'
    get_content.admin_order_field = 'content.content_key'

    def get_created_at(self, obj: UserFavorite):
        return obj.created_at
    get_created_at.short_description = '收藏时间'
    get_created_at.admin_order_field = 'created_at'

    class ProxyResource(resources.ModelResource):
        class Meta:
            model = UserFavorite
    resource_class = ProxyResource

admin.site.register(UserFavorite, UserFavoriteAdmin)

# 用户学习行为管理
class UserLearningBehaviorAdmin(ImportExportModelAdmin):
    list_display = [
        'get_user', 'get_last_learning_time_interval', 'get_study_frequency', 'get_topic_proficiency',
        'get_active_time_distribution', 'get_content_click_rate', 'get_updated_at'
    ]
    list_per_page = 10
    list_filter = ['last_learning_time_interval', 'updated_at']
    search_fields = ['user__username']
    ordering = ['-updated_at']

    def get_user(self, obj: UserLearningBehavior):
        return obj.user.username
    get_user.short_description = '用户名'
    get_user.admin_order_field = 'user__username'

    def get_last_learning_time_interval(self, obj: UserLearningBehavior):
        return obj.get_last_learning_time_interval_display()
    get_last_learning_time_interval.short_description = '最近学习时间间隔'
    get_last_learning_time_interval.admin_order_field = 'last_learning_time_interval'

    def get_study_frequency(self, obj: UserLearningBehavior):
        return format_html(",".join([f"<b>{key}</b>: {value}" for key, value in obj.study_frequency_last_7_days.items()]) if obj.study_frequency_last_7_days.items() else '暂无')
    get_study_frequency.short_description = '过去7天学习频率'

    def get_active_time_distribution(self, obj: UserLearningBehavior):
        return format_html(",".join([f"<b>{key}</b>: {value}" for key, value in obj.active_time_distribution.items()]) if obj.active_time_distribution.items() else '暂无')
    get_active_time_distribution.short_description = '活跃时间分布'

    def get_updated_at(self, obj: UserLearningBehavior):
        return obj.updated_at
    get_updated_at.short_description = '最近更新时间'
    get_updated_at.admin_order_field = 'updated_at'

    def get_content_click_rate(self, obj: UserLearningBehavior):
        return format_html(",".join([f"<b>{key}</b>: {value * 100}%" for key, value in obj.content_click_rate.items()]) if obj.content_click_rate.items() else '暂无')
    get_content_click_rate.short_description = '用户点击率'
    get_content_click_rate.admin_order_field = 'content_click_rate'

    def get_topic_proficiency(self, obj: UserLearningBehavior):
        return format_html(",".join([f"<b>{key}</b>: {value}" for key, value in obj.topic_proficiency.items()]) if obj.topic_proficiency.items() else '暂无')
    get_topic_proficiency.short_description = '考点熟练度'

    def changelist_view(self, request, extra_context=None):
        # 当访问管理界面时，更新所有用户的学习间隔
        user_behaviors = UserLearningBehavior.objects.all()
        for user_behavior in user_behaviors:
            user_behavior.update_last_learning_interval()

        # 调用原有的 changelist_view 以保持正常的管理界面功能
        return super().changelist_view(request, extra_context)

    class ProxyResource(resources.ModelResource):
        class Meta:
            model = UserLearningBehavior
    resource_class = ProxyResource

admin.site.register(UserLearningBehavior, UserLearningBehaviorAdmin)