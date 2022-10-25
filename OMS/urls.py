"""OMS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from deploy.views import depart, user, account

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('deploy_add/', user.user_add()),

    # 部门管理
    path('depart/list/', depart.depart_list),
    path('depart/add/', depart.depart_add),
    path('depart/delete/', depart.depart_delete),
    path('depart/edit/', depart.depart_edit),
    path('depart/detail/', depart.depart_detail),

    # 用户管理
    path('user/add/', user.user_add),
    path('user/list/', user.user_list),
    path('user/<int:nid>/edit/', user.user_edit),
    path('user/delete/', user.user_delete),  # 点击删除后，需要点确认才删除
    # path('user/<int:nid>/delete/', user.user_delete),          # 不需要确认，点击删除直接删除

    # 用户登录
    path('login/', account.login),
    path('image/code/', account.image_code),
    path('logout/', account.logout),

]
