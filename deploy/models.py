import django.utils.timezone

from django.db import models
from datetime import datetime


class UserInfo(models.Model):
    """用户信息表"""
    user_account = models.CharField(verbose_name='用户名', max_length=32)
    user_name = models.CharField(verbose_name='姓名', max_length=32)
    user_password = models.CharField(verbose_name='密码', max_length=32)
    # create_time = models.DateField(verbose_name="创建时间")
    depart = models.ForeignKey(verbose_name="部门", to="Department", to_field="id", on_delete=models.DO_NOTHING,
                               default=None)
    user_email = models.EmailField(verbose_name='邮箱', blank=True, null=True, default='')
    # 在django中做的约束,性别选择项
    gender_choices = (
        (1, "男"),
        (2, "女"),
    )
    user_gender = models.SmallIntegerField(verbose_name='性别', choices=gender_choices)
    # 用户状态选择项
    user_status_choices = (
        (1, "启用"),
        (0, "停用"),
    )
    user_status = models.SmallIntegerField(verbose_name='状态', choices=user_status_choices, default=1)
    create_time = models.DateField(verbose_name='创建时间', default=datetime.today)

    def __str__(self):
        return self.user_name


class ProdInfo(models.Model):
    """产品信息表"""
    prod_name = models.CharField(verbose_name='产品名称', max_length=100)
    # 级联删除，即：如果删除用户表中的该用户信息，则条数据也要跟着删除
    # prod_owner = models.ForeignKey(verbose_name='产品经理', to=user_info, to_field=user_info.user_name,
    #                                on_delete=models.CASCADE)
    # 删除用户表中的该用户信息，什么也不做，即不影响产品表中的数据
    prod_owner = models.ForeignKey(verbose_name='产品经理', to=UserInfo, to_field='id',
                                   on_delete=models.DO_NOTHING)


class DeployInfo(models.Model):
    """部署信息表"""
    prod_name = models.CharField(verbose_name='产品名称', max_length=100)
    prod_version = models.CharField(verbose_name='版本号', max_length=100)
    deploy_user = models.ForeignKey(verbose_name='部署人员', to=UserInfo, to_field='id',
                                    on_delete=models.DO_NOTHING)
    deploy_site = models.CharField(verbose_name='部署地点', max_length=256)
    deploy_date = models.DateField(verbose_name='部署时间', default=datetime.today)
    deploy_expiry_date = models.DateField(verbose_name='失效时间', default=datetime.today)
    deploy_remark: str = models.TextField(verbose_name='补充说明', max_length=256, null=True, blank=True)


class Department(models.Model):
    """部署信息表"""
    depart_name = models.CharField(verbose_name='部门名称', max_length=32)

    def __str__(self):
        return self.depart_name


# class UrlGroup(models.Model):
#     """ URL 分组信息表 """
#     group_name = models.CharField(verbose_name='分组名称', max_length=32)
#
#     def __str__(self):
#         return self.group_name
#
#
# class UrlBar(models.Model):
#     """ URL 地址记录信息表 """
#     url_name = models.CharField(verbose_name='URL名称', max_length=32)
#     url_address = models.URLField(verbose_name='URL地址')
#     url_group = models.ForeignKey(verbose_name="URL分组", to="UrlGroup", to_field="id", on_delete=models.CASCADE)