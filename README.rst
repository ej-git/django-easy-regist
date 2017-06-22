==================
django-easy-regist
==================

.. image:: https://travis-ci.org/naritotakizawa/django-easy-regist.svg?branch=master
    :target: https://travis-ci.org/naritotakizawa/django-easy-regist

.. image:: https://coveralls.io/repos/github/naritotakizawa/django-easy-regist/badge.svg?branch=master
    :target: https://coveralls.io/github/naritotakizawa/django-easy-regist?branch=master

仮登録、メールで本登録URLの送付、パスワードの再設定、等の一連のサンプルアプリケーション


Requirement
--------------

:Python: 3.5以上
:Django: 1.11以上


Quick start
-----------

1. settings.pyの編集 ::

    INSTALLED_APPS = [
        ...
        'easy_regist',  # add
    ]

    # ログインURL等の設定例
    LOGIN_URL = "easy_regist:login"
    LOGIN_REDIRECT_URL = 'easy_regist:index'
     
    # メールの設定例(gmail)
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_PORT = 587
    EMAIL_HOST_USER = 'your_gmail_acount'
    EMAIL_HOST_PASSWORD = 'your_gmail_password'
    EMAIL_USE_TLS = True

    # カスタムなユーザーモデルを利用する
    AUTH_USER_MODEL = 'easy_regist.User'

2. urls.pyに足す::

    url(r'^regist/', include('easy_regist.urls')),

3. python manage.py migrate　でカスタムUserモデルを追加する.

4. http://127.0.0.1:8000/regist/ へ.