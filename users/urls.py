from django.urls import path
from .views import (register_user, login_user, refresh_token, auto_login,
                    leaderboard_inquiry, get_exams, update_user, save_user_history, load_user_history,
                    log_user_activity, test_front_back_connection, label_encoder)

app_name = 'users'
urlpatterns = [
    path("register/", register_user, name="register"), # 注册用户
    path("login/", login_user, name="login"),
    path("token/refresh/", refresh_token, name="token_refresh"),
    path("token/auto-login/", auto_login, name="token_auto_login"),
    path("update/", update_user, name="update_user"),
    path("get-leaderboard", leaderboard_inquiry, name="get_leaderboard"),
    path('exams/', get_exams, name="exam_list"),
    path('save-history/', save_user_history, name="save_user_history"),
    path('load-history/', load_user_history, name="load_user_history"),
    path('log-user-activity/', log_user_activity, name="log_user_activity"),
    path('test/', test_front_back_connection, name="test_front_back_connection"),
    path('label-encoder/', label_encoder, name="label_encoder"),
]