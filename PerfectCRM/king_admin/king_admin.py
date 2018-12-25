from django.contrib import admin
from crm import models
# {'crm':{'表名':admin_class}}  先定义为空
enabled_admins = {}


class BaseAdmin(object):
    list_display = []
    list_filters = []
    search_fields = []
    ordering = None
    filter_horizontal = ()  # 增加复选框
    actions = []

class CustomerAdmin(BaseAdmin):
    list_display = ['id', 'name', 'qq', 'source', 'consultant', 'consult_course', 'content', 'date']
    list_filters = ['source', 'consultant', 'consult_course', 'date']
    search_fields = ['name', 'qq',]
    filter_horizontal = ('tags',)  # 增加复选框
    list_per_page = 2
    ordering = 'id'
    actions = ['delete_selected_objs',]

    def delete_selected_objs(self,request,querysets):
        print('def delete_selected_objs',self,request,querysets)

class CustomerFollowUpAdmin(BaseAdmin):
    list_display = ['customer','consultant','intantion','date']
    list_per_page = 2

def register(model_class, admin_class=None):
    # modle_class._meta.app_lable 得到的是app的名字
    if model_class._meta.app_label not in enabled_admins:
        enabled_admins[model_class._meta.app_label] = {}

    # 把表对象与 admin_class 绑定在一起
    admin_class.model = model_class
    enabled_admins[model_class._meta.app_label][model_class._meta.model_name] = admin_class


register(models.Customer, CustomerAdmin)
register(models.CustomerFollowUp, CustomerFollowUpAdmin)

