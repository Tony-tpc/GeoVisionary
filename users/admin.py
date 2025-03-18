from django.contrib import admin
from django.utils.html import format_html
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import FrontendUser,Category,ExamSet,Problem,UserHistory,UserConversation,APIConfig

# 用户管理
class FrontendUserAdmin(admin.ModelAdmin):
    # 指定展示的内容
    list_display = ['get_user_id','get_username','get_email','get_gender','get_grade','get_remarks','get_correct_problems','get_avatar','get_created_at']

    # 指定一页显示多少条数据
    list_per_page = 20

    # 过滤器
    list_filter = ['gender','grade','created_at']

    # 搜索框
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
    get_remarks.admin_order_field = 'remarks'

    def get_correct_problems(self,obj:FrontendUser):
        return obj.correct_problems
    get_correct_problems.short_description = '正确题目数'
    get_correct_problems.admin_order_field = 'correct_problems'

    def get_avatar(self,obj:FrontendUser):
        return obj.avatar
    get_avatar.short_description = '头像'
    get_avatar.admin_order_field = 'avatar'

    def get_created_at(self,obj:FrontendUser):
        return obj.created_at
    get_created_at.short_description = '注册时间'
    get_created_at.admin_order_field = 'created_at'

admin.site.register(FrontendUser,FrontendUserAdmin)

# 分类管理
class CategoryAdmin(admin.ModelAdmin):
    # 指定展示内容
    list_display = ['get_name','get_category_type']

    # 指定一页显示多少条数据
    list_per_page = 10

    # 过滤器
    list_filter = ['category_type']

    # 搜索框
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

admin.site.register(Category,CategoryAdmin)

# 试题组管理
class ExamSetAdmin(ImportExportModelAdmin):
    # 指定展示内容
    list_display = ['id','get_title','get_description','get_image_preview','get_categories','get_created_at']

    # 指定一页显示多少条数据
    list_per_page = 10

    # 过滤器
    list_filter = ['categories','created_at']

    # 搜索框
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
    get_description.admin_order_field = 'description'

    def get_image_preview(self, obj: ExamSet):
        if obj.image:
            return format_html('<img src="{}" width="100px" height="auto"/>', obj.image.url)
        return "无图片"
    get_image_preview.short_description = '图片预览'

    def get_created_at(self, obj: ExamSet):
        return obj.created_at
    get_created_at.short_description = '建立时间'
    get_created_at.admin_order_field = 'created_at'

    # 自定义导入导出行为
    class ProxyResource(resources.ModelResource):
        class Meta:
            model = ExamSet
    resource_class = ProxyResource

admin.site.register(ExamSet,ExamSetAdmin)

# 试题表管理
class ProblemAdmin(ImportExportModelAdmin):
    # 显示展示内容
    list_display = ['id','get_exam_set','get_question_number','get_question','get_choices_formatted','get_answer','get_explanation','get_categories','get_created_at']

    # 指定一页显示多少条数据
    list_per_page = 10

    # 过滤器
    list_filter = ['created_at','categories']

    # 搜索框
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
    get_explanation.admin_order_field = 'explanation'

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
    # 指定展示内容
    list_display = ['get_frontend_user','get_precursor_id','get_session_id','get_timestamp','get_user_message','get_llm_response']

    # 指定一页显示多少条数据
    list_per_page = 10

    # 搜索框
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
    get_user_message.admin_order_field = 'user_message'

    def get_llm_response(self, obj: UserConversation):
        return obj.llm_response
    get_llm_response.short_description = 'llm输出'
    get_llm_response.admin_order_field = 'llm_response'

admin.site.register(UserConversation,UserConversationAdmin)

class APIConfigAdmin(admin.ModelAdmin):
    # 指定展示内容
    list_display = ['get_service_name','get_api_key','get_api_secret','get_app_id','get_host','get_path','get_created_at','get_last_used_at','get_usage_count','get_is_active']

    # 指定一页展示的内容
    list_per_page = 10

    # 过滤器
    list_filter = ['service_name','is_active']

    # 搜索框
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
    get_api_secret.admin_order_field = 'api_secret'

    def get_app_id(self, obj: APIConfig):
        return obj.app_id
    get_app_id.short_description = 'App ID'
    get_app_id.admin_order_field = 'app_id'

    def get_host(self, obj: APIConfig):
        return obj.host
    get_host.short_description = '服务器地址'
    get_host.admin_order_field = 'host'

    def get_path(self, obj: APIConfig):
        return obj.path
    get_path.short_description = '访问路径'
    get_path.admin_order_field = 'path'

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
