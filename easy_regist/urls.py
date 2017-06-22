from django.conf.urls import url
from . import views

app_name = 'easy_regist'

urlpatterns = [

    # トップページ
    url(r'^$', views.TopPageView.as_view(), name='index'),

    # マイページ機能
    url(r'^mypage/$', views.MyPageView.as_view(), name='mypage'),
    url(r'^user_update/(?P<pk>[0-9]+)/$',
        views.UserUpdateView.as_view(), name='user_update'),
    url(r'^change_password/$', views.PasswordChangeView.as_view(), name='change_password'),
    url(r'^change_password_done/$', views.PasswordChangeDoneView.as_view(),
        name='change_password_done'),

    # 会員登録
    url(r'^create/$', views.CreateUserView.as_view(), name='create'),
    url(r'^create_done/$', views.CreateDoneView.as_view(), name='create_done'),
    url(r'^create_complete/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.CreateCompleteView.as_view(), name='create_complete'),

    # ログイン、ログアウト
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),

    # パスワード忘れ
    url(r'^password_reset/$', views.PasswordResetView.as_view(), name='password_reset'),
    url(r'^password_reset_done/$', views.PasswordResetDoneView.as_view(),
        name='password_reset_done'),
    url(r'^password_reset_confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    url(r'^password_reset_complete/$', views.PasswordResetCompleteView.as_view(),
        name='password_reset_complete'),
]
