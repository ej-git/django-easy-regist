from django.http import Http404
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import generic

from .models import User
from .forms import (
    RegisterForm,
    LoginForm,
    UpdateForm,
    ChangePasswordForm,
    ForgetPasswordForm,
    PasswordConfirmForm
)


class TopPageView(generic.TemplateView):
    """トップページ."""

    template_name = 'easy_regist/index.html'


class MyPageView(LoginRequiredMixin, generic.TemplateView):
    """マイページ."""

    template_name = 'easy_regist/info.html'


class UserUpdateView(LoginRequiredMixin, generic.UpdateView):
    """ユーザー情報更新ページ."""

    model = User
    form_class = UpdateForm
    success_url = reverse_lazy('easy_regist:mypage')
    template_name = 'easy_regist/user_update.html'


class PasswordChangeView(LoginRequiredMixin, auth_views.PasswordChangeView):
    """パスワード変更ページ."""

    form_class = ChangePasswordForm
    success_url = reverse_lazy('easy_regist:change_password_done')
    template_name = 'easy_regist/change_password.html'


class PasswordChangeDoneView(
        LoginRequiredMixin, auth_views.PasswordChangeDoneView):
    """パスワード変更完了ページ."""

    template_name = 'easy_regist/change_password_done.html'


class CreateUserView(generic.FormView):
    """ユーザー登録ページ."""

    template_name = 'easy_regist/create.html'
    form_class = RegisterForm
    success_url = reverse_lazy('easy_regist:create_done')

    def form_valid(self, form):
        """仮登録と本登録用メールの発行."""
        user = form.save()

        current_site = get_current_site(self.request)
        domain = current_site.domain

        subject_template = get_template(
            'easy_regist/mailtemplate/new/subject.txt')
        message_template = get_template(
            'easy_regist/mailtemplate/new/message.txt')

        context = {
            'protocol': 'https' if self.request.is_secure() else 'http',
            'domain': domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
            'user': user,
        }

        subject = subject_template.render(context)
        message = message_template.render(context)
        from_email = settings.EMAIL_HOST_USER
        to = [user.email]

        send_mail(subject, message, from_email, to)
        return super().form_valid(form)


class CreateDoneView(generic.TemplateView):
    """仮登録しましたページ."""

    template_name = 'easy_regist/create_done.html'


class CreateCompleteView(generic.TemplateView):
    """登録は全て完了しましたページ."""

    template_name = 'easy_regist/create_complete.html'

    def get(self, request, **kwargs):
        """uid、tokenが正しければ本登録."""
        token = kwargs.get('token')
        uidb64 = kwargs.get('uidb64')
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user and user.is_active:
            if default_token_generator.check_token(user, token):
                user.is_active = True
                user.save()
                return super().get(request, **kwargs)

        raise Http404


class PasswordResetView(auth_views.PasswordResetView):
    """パスワード変更用URLの送付ページ."""

    email_template_name = 'easy_regist/mailtemplate/password_reset/message.txt'
    form_class = ForgetPasswordForm
    subject_template_name = \
        'easy_regist/mailtemplate/password_reset/subject.txt'
    success_url = reverse_lazy('easy_regist:password_reset_done')
    template_name = 'easy_regist/password_reset_form.html'


class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    """パスワード変更用URLを送りましたページ."""

    template_name = 'easy_regist/password_reset_done.html'


class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    """新パスワード入力ページ."""

    form_class = PasswordConfirmForm
    success_url = reverse_lazy('easy_regist:password_reset_complete')
    template_name = 'easy_regist/password_reset_confirm.html'


class PasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    """新パスワード設定しましたページ."""

    template_name = 'easy_regist/password_reset_complete.html'


class LoginView(auth_views.LoginView):
    """ログインページ."""

    form_class = LoginForm
    template_name = 'easy_regist/login.html'


class LogoutView(LoginRequiredMixin, auth_views.LogoutView):
    """ログアウトページ."""

    template_name = 'easy_regist/index.html'
