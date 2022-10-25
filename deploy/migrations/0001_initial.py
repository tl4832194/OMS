# Generated by Django 4.1.1 on 2022-09-25 20:48

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('depart_name', models.CharField(max_length=32, verbose_name='部门名称')),
            ],
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_account', models.CharField(max_length=32, verbose_name='用户名')),
                ('user_name', models.CharField(max_length=32, verbose_name='姓名')),
                ('user_password', models.CharField(max_length=32, verbose_name='密码')),
                ('user_email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='邮箱')),
                ('user_gender', models.SmallIntegerField(choices=[(1, '男'), (2, '女')], verbose_name='性别')),
                ('user_status', models.SmallIntegerField(choices=[(1, '启用'), (0, '停用')], default=1, verbose_name='状态')),
                ('depart', models.ForeignKey(default=None, on_delete=django.db.models.deletion.DO_NOTHING, to='deploy.department', verbose_name='部门')),
            ],
        ),
        migrations.CreateModel(
            name='ProdInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prod_name', models.CharField(max_length=100, verbose_name='产品名称')),
                ('prod_owner', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='deploy.userinfo', verbose_name='产品经理')),
            ],
        ),
        migrations.CreateModel(
            name='DeployInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prod_name', models.CharField(max_length=100, verbose_name='产品名称')),
                ('prod_version', models.CharField(max_length=100, verbose_name='版本号')),
                ('deploy_site', models.CharField(max_length=256, verbose_name='部署地点')),
                ('deploy_date', models.DateField(default=datetime.datetime.today, verbose_name='部署时间')),
                ('deploy_expiry_date', models.DateField(default=datetime.datetime.today, verbose_name='失效时间')),
                ('deploy_remark', models.TextField(blank=True, max_length=256, null=True, verbose_name='补充说明')),
                ('deploy_user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='deploy.userinfo', verbose_name='部署人员')),
            ],
        ),
    ]