from django.shortcuts import render, redirect
from django.http import HttpResponse
from io import BytesIO
from django import forms

from deploy.utils.form import LoginForm
from deploy import models
from deploy.utils.code import check_code


# from deploy.utils.bootstrap import BootStrapForm


def image_code(request):
    """ 生成图片验证码 """

    # 调用pillow函数，生成图片
    img, code_string = check_code()

    # 写入到自己的session中（以便于后续获取验证码再进行校验）
    request.session['image_code'] = code_string
    # 给Session设置60s超时
    request.session.set_expiry(60)

    stream = BytesIO()
    img.save(stream, 'png')
    return HttpResponse(stream.getvalue())


def login(request):
    """ 用户登录 """
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'login.html', {'form': form})
    form = LoginForm(data=request.POST)
    # print("form is {}".format(form))
    if form.is_valid():
        # 验证码的校验
        user_input_code = form.cleaned_data.pop('code')
        code = request.session.get('image_code', "")
        # print("222222", form.cleaned_data)
        if code.upper() != user_input_code.upper():
            form.add_error("code", "验证码错误")
            return render(request, 'login.html', {'form': form})

        # 去数据库校验用户名和密码是否正确，获取用户对象、None
        # admin_object = models.Admin.objects.filter(username=xxx, password=xxx).first()
        account_object = models.UserInfo.objects.filter(**form.cleaned_data).first()
        if not account_object:
            form.add_error("user_password", "用户名或密码错误")
            # form.add_error("username", "用户名或密码错误")
            return render(request, 'login.html', {'form': form})

        # 用户名和密码正确
        # 网站生成随机字符串; 写到用户浏览器的cookie中；在写入到session中；
        request.session["info"] = {'id': account_object.id, 'account': account_object.user_account,
                                   'username': account_object.user_name}
        # session可以保存7天
        # request.session.set_expiry(60 * 60 * 24 * 7)
        request.session.set_expiry(60 * 60 * 24)

        return redirect("/user/list/")

    return render(request, 'login.html', {'form': form})


def logout(request):
    """ 注销 """
    request.session.clear()
    return redirect("/login/")
