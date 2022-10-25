from django.shortcuts import render, redirect
from django.http import JsonResponse
from deploy import models
from deploy.utils.pagination import Pagination

from django import forms
from django.core.exceptions import ValidationError
from deploy.utils.bootstrap import BootStrapModelForm
from deploy.utils.form import UserModelForm
from deploy.utils.encrypt import md5


def user_add(request):
    """ 添加用户 """
    if request.method == 'GET':
        # 用于获取数据模型字段，并展示在页面上，因为我们的model_form中的fields = ['depart_name']，所以我们只展示部门名称这个字段
        form = UserModelForm()
        # 将获取的字段展示到html页面上
        return render(request, 'user_add.html', {'form': form})
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        # 如果数据合法，则将获取到的数据全部保存到数据库中
        form.save()
        return redirect('/user/list/')
    # 校验失败（在页面上显示错误信息）
    return render(request, 'user_add.html', {"form": form})


def user_list(request):
    """ 用户列表 """
    queryset = models.UserInfo.objects.all()
    # 分页
    page_object = Pagination(request, queryset)
    form = UserModelForm()
    context = {
        'form': form,
        "queryset": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html()  # 生成页码
    }
    # 将部门数据返回给html页面进行展示
    return render(request, 'user_list.html', context)


def user_edit(request, nid):
    """ 用户编辑 """
    # 根据nid获取用户编号所对应那一行的数据
    row_obj = models.UserInfo.objects.filter(id=nid).first()

    if not row_obj:
        return redirect('/user/list/')

    # 进入修改页面
    if request.method == 'GET':
        form = UserModelForm(instance=row_obj)
        return render(request, 'user_edit.html', {"form": form})
    form = UserModelForm(data=request.POST, instance=row_obj)

    # 校验输入的数据的合法性
    if form.is_valid():
        form.save()
        return redirect('/user/list')
    return render(request, 'user_edit.html', {"form": form})


# def user_delete(request, nid):
#     """ 直接删除用户，不需要确认 """
#     # row_obj = models.UserInfo.objects.filter(id=nid).first()
#     # if not row_obj:
#     #     return redirect('/user/list')
#     models.UserInfo.objects.filter(id=nid).delete()
#     return redirect('/user/list')

def user_delete(request):
    """ 删除用户前，需要先弹出确认框，点击确认才删除 """
    uid = request.GET.get('uid')
    exists = models.UserInfo.objects.filter(id=uid).exists()
    if not exists:
        return JsonResponse({"status": False, "error": "用户信息不存在"})
    models.UserInfo.objects.filter(id=uid).delete()
    return JsonResponse({"status": "True"})
