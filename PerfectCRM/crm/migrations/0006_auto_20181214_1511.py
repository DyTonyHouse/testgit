# Generated by Django 2.1.2 on 2018-12-14 07:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0005_auto_20181214_1435'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='roles',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='roles',
            field=models.ManyToManyField(blank=True, null=True, to='crm.Role'),
        ),
    ]
