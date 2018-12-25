# Generated by Django 2.1.2 on 2018-12-14 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0004_role_menus'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu',
            name='url_name',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.RemoveField(
            model_name='role',
            name='menus',
        ),
        migrations.AddField(
            model_name='role',
            name='menus',
            field=models.ManyToManyField(to='crm.Menu'),
        ),
    ]