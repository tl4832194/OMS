from deploy import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django import forms
from deploy.utils.bootstrap import BootStrapModelForm, BootStrapForm
from deploy.utils.encrypt import md5


class DepartModelForm(BootStrapModelForm):
    """ 部门校验模型 """
    depart_name = forms.CharField(
        # 用于生成html标签时，页面展示的标题
        label="部门名称",
        # 生成的html页面会生成一个input输入框
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = models.Department
        fields = ["depart_name"]

    # 验证部门名称是否存在
    def clean_depart_name(self):
        # 当前编辑的哪一行的ID
        # print(self.instance.pk)
        txt_depart_name = self.cleaned_data["depart_name"]
        exists = models.Department.objects.exclude(id=self.instance.pk).filter(depart_name=txt_depart_name).exists()
        if exists:
            raise ValidationError("部门名称已经存在")

        # 验证通过，用户输入的值返回
        return txt_depart_name


class UserModelForm(BootStrapModelForm):
    """ 用户校验模型 """

    # user_account = forms.CharField(
    #     max_length=32,
    #     label="用户名",
    #     widget=forms.TextInput(attrs={"class": "form-control"})
    # )

    # 新增"确认密码"字段，该字段在数据库是不存在的
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(render_value=True)
    )

    class Meta:
        model = models.UserInfo
        fields = ["user_account", "user_name", "user_password", "confirm_password", "user_email", "user_status",
                  "user_gender", "depart"]
        # exclude = ["create_time"]
        # 定义密码字段在页面展示的样式，展示为密码保护格式
        widgets = {
            "user_password": forms.PasswordInput(render_value=True)
        }

    def clean_user_password(self):
        pwd = self.cleaned_data.get("user_password")
        return md5(pwd)

    # 校验用户名
    def clean_user_account(self):
        # 当前编辑的哪一行的ID
        # print(self.instance.pk)
        txt_user_account = self.cleaned_data["user_account"]
        exists = models.UserInfo.objects.exclude(id=self.instance.pk).filter(user_account=txt_user_account).exists()
        if exists:
            raise ValidationError("用户名已经存在")

        # 验证通过，用户输入的值返回
        return txt_user_account

    # 校验用户密码
    def clean_user_password(self):
        pwd = self.cleaned_data.get("user_password")
        md5_pwd = md5(pwd)

        # 去数据库校验当前密码和新输入的密码是否一致
        exists = models.UserInfo.objects.filter(id=self.instance.pk, user_password=md5_pwd).exists()
        if exists:
            raise ValidationError("不能与以前的密码相同")

        return md5_pwd

    # 校验确认密码
    def clean_confirm_password(self):
        pwd = self.cleaned_data.get("user_password")
        confirm = md5(self.cleaned_data.get("confirm_password"))
        if confirm != pwd:
            raise ValidationError("密码不一致")
        # 返回什么，此字段以后保存到数据库就是什么。
        return confirm


class UserResetModelForm(BootStrapModelForm):
    """ 重置密码模型 """
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(render_value=True)
    )

    class Meta:
        model = models.UserInfo
        fields = ['user_password', 'confirm_password']
        widgets = {
            "user_password": forms.PasswordInput(render_value=True)
        }

    def clean_user_password(self):
        pwd = self.cleaned_data.get("user_password")
        md5_pwd = md5(pwd)

        # 去数据库校验当前密码和新输入的密码是否一致
        exists = models.UserInfo.objects.filter(id=self.instance.pk, user_password=md5_pwd).exists()
        if exists:
            raise ValidationError("不能与以前的密码相同")

        return md5_pwd

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get("user_password")
        confirm = md5(self.cleaned_data.get("confirm_password"))
        if confirm != pwd:
            raise ValidationError("密码不一致")
        # 返回什么，此字段以后保存到数据库就是什么。
        return confirm


class LoginForm(BootStrapForm):
    """ 用户登录模型 """
    user_account = forms.CharField(
        label="用户名",
        widget=forms.TextInput,
        required=True
    )
    user_password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput(render_value=True),
        required=True
    )

    code = forms.CharField(
        label="验证码",
        widget=forms.TextInput,
        required=True
    )

    def clean_user_password(self):
        pwd = self.cleaned_data.get("user_password")
        # print("1111111", md5(pwd))
        return md5(pwd)

#
# class PrettyModelForm(BootStrapModelForm):
#     # 验证：方式1
#     mobile = forms.CharField(
#         label="手机号",
#         validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误'), ],
#     )
#
#     class Meta:
#         model = models.PrettyNum
#         # fields = "__all__"
#         # exclude = ['level']
#         fields = ["mobile", 'price', 'level', 'status']
#
#     # 验证：方式2
#     def clean_mobile(self):
#         txt_mobile = self.cleaned_data["mobile"]
#
#         exists = models.PrettyNum.objects.filter(mobile=txt_mobile).exists()
#         if exists:
#             raise ValidationError("手机号已存在")
#
#         # 验证通过，用户输入的值返回
#         return txt_mobile
#
#
# class PrettyEditModelForm(BootStrapModelForm):
#     # mobile = forms.CharField(disabled=True, label="手机号")
#     mobile = forms.CharField(
#         label="手机号",
#         validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误'), ],
#     )
#
#     class Meta:
#         model = models.PrettyNum
#         fields = ['mobile', 'price', 'level', 'status']
#
#     # 验证：方式2
#     def clean_mobile(self):
#         # 当前编辑的哪一行的ID
#         # print(self.instance.pk)
#         txt_mobile = self.cleaned_data["mobile"]
#         exists = models.PrettyNum.objects.exclude(id=self.instance.pk).filter(mobile=txt_mobile).exists()
#         if exists:
#             raise ValidationError("手机号已存在")
#
#         # 验证通过，用户输入的值返回
#         return txt_mobile
