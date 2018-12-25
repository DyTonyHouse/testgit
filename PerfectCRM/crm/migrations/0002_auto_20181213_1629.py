# Generated by Django 2.1.4 on 2018-12-13 08:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='branch',
            options={'verbose_name_plural': '校区'},
        ),
        migrations.AlterModelOptions(
            name='classlist',
            options={'verbose_name_plural': '班级'},
        ),
        migrations.AlterModelOptions(
            name='course',
            options={'verbose_name_plural': '课程'},
        ),
        migrations.AlterModelOptions(
            name='courserecord',
            options={'verbose_name_plural': '上课记录'},
        ),
        migrations.AlterModelOptions(
            name='customer',
            options={'verbose_name_plural': '客户信息'},
        ),
        migrations.AlterModelOptions(
            name='customerfollowup',
            options={'verbose_name_plural': '客户跟进状况'},
        ),
        migrations.AlterModelOptions(
            name='enrollment',
            options={'verbose_name_plural': '报名表'},
        ),
        migrations.AlterModelOptions(
            name='payment',
            options={'verbose_name_plural': '消费记录'},
        ),
        migrations.AlterModelOptions(
            name='role',
            options={'verbose_name_plural': '角色'},
        ),
        migrations.AlterModelOptions(
            name='studyrecord',
            options={'verbose_name_plural': '学习记录'},
        ),
        migrations.AlterModelOptions(
            name='tag',
            options={'verbose_name_plural': '标签'},
        ),
        migrations.AlterModelOptions(
            name='userprofile',
            options={'verbose_name_plural': '账号'},
        ),
    ]