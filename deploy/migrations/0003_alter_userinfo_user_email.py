# Generated by Django 4.1.1 on 2022-09-26 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deploy', '0002_userinfo_create_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='user_email',
            field=models.EmailField(blank=True, default='', max_length=254, null=True, verbose_name='邮箱'),
        ),
    ]
