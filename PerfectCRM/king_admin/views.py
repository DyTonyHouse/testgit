from django.shortcuts import render,redirect,reverse
from king_admin import utils
from . import forms
# Create your views here.

from king_admin import king_admin
def index(request):
    # print(king_admin.enabled_admins['crm']['customer'].model.objects.ge)
    table_list = king_admin.enabled_admins
    return render(request, 'king_admin/table_index.html', {'table_list':table_list})


def display_table(request,app_name,table_name):
    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
    # admin_class规定了显示的内容，并且还有model属性，所以将admin_class传入前端
    admin_class = king_admin.enabled_admins[app_name][table_name]

    # <!--分页功能>
    # 得到表的对象的列表，因为 Paginator 第一个参数必须是可迭代的，第二个参数是每页展示的个数
    # model_all = admin_class.model.objects.all()
    models_list,filter_conditions = utils.table_filter(request, admin_class)      # 过滤后

    models_list, search_key = utils.table_search(request, models_list, admin_class)     # 搜索后

    models_list, orderby_key = utils.table_sort(request, models_list)      # 排序后

    # 传入 list_per_page 作为每页的数据量，保证检索前与检索后展示相同的数据量
    paginator = Paginator(models_list,admin_class.list_per_page)
    current_page = request.GET.get('page')

    try:
        # paginator.page()得到的是一页的对象列表，所以前端不用再对
        # admin_class.model.objects.all()进行循环，而是循环posts
        posts = paginator.page(current_page)

    # 防止用户输入非法字符
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request,'king_admin/table_obj.html',{'admin_class':admin_class,
                                                       'posts':posts,
                                                       'filter_conditions':filter_conditions,
                                                       'orderby_key':orderby_key,
                                                       'search_key':search_key,
                                                       'request':request})


def table_obj_change(request,app_name,table_name,obj_id):
    admin_class = king_admin.enabled_admins[app_name][table_name]

    model_form_class = forms.create_model_form(request, admin_class)

    obj = admin_class.model.objects.get(id=obj_id)

    if request.method == 'POST':
        form_obj = model_form_class(request.POST, instance=obj)

        # 前端填写的数据没有异常就保存
        if form_obj.is_valid():
            form_obj.save()
            return redirect(reverse('table_obj',kwargs={'app_name':app_name,'table_name':table_name}))
    else:
        form_obj = model_form_class(instance=obj)

    return render(request, 'king_admin/table_obj_change.html', {'form_obj':form_obj,
                                                                'admin_class':admin_class,
                                                                'app_name':app_name,
                                                                'table_name':table_name})


def table_obj_add(request, app_name, table_name):
    admin_class = king_admin.enabled_admins[app_name][table_name]

    model_form_class = forms.create_model_form(request, admin_class)


    if request.method == 'POST':
        form_obj = model_form_class(request.POST)

        # 前端填写的数据没有异常就保存
        if form_obj.is_valid():
            form_obj.save()
            return redirect(reverse('table_obj', kwargs={'app_name': app_name, 'table_name': table_name}))
    else:
        form_obj = model_form_class()
    return render(request, 'king_admin/table_obj_add.html', {'form_obj':form_obj,
                                                             'admin_class':admin_class,
                                                             'app_name': app_name,
                                                             'table_name': table_name})


def table_obj_delete(request, app_name, table_name, model_obj_id):
    admin_class = king_admin.enabled_admins[app_name][table_name]
    model_obj = admin_class.model.objects.get(id=model_obj_id)

    if request.method == 'POST':
        print('11111sssss')
        model_obj.delete()
        return redirect(reverse('table_obj', kwargs={'app_name': app_name, 'table_name': table_name}))

    return render(request, 'king_admin/table_obj_delete.html', {'model_obj':model_obj,
                                                                'app_name':app_name,
                                                                'table_name':table_name,
                                                                'model_obj_id':model_obj_id})