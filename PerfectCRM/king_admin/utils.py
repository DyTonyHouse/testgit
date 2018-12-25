from django.db.models import Q
from django.utils.timezone import datetime, timedelta

def table_filter(request,admin_class):
    '''进行条件过滤并返回过滤后的数据'''
    filter_conditions = {}

    keyword = ['page', 'o', '_q']       # filter_conditions过滤字段里不能出现的url

    for k,v in request.GET.items():
        if k in keyword:
            continue
        if v:
            filter_conditions[k] = v

    return admin_class.model.objects.filter(**filter_conditions).order_by('-%s'%admin_class.ordering if admin_class.ordering else '-id'), filter_conditions


def table_sort(request, models_list):
    orderby_key = request.GET.get('o')

    if orderby_key:
        models_list = models_list.order_by(orderby_key)

    return models_list, orderby_key


def table_search(request, models_list, admin_class):
    search_key = request.GET.get('_q','')

    q_obj = Q()
    q_obj.connector = 'OR'      # 指定过滤方式是 ’或‘

    for search_field in admin_class.search_fields:          # 把搜索内容_q 与每个search字段都组成一个元组
        q_obj.children.append(('%s__contains'%search_field, search_key))

    return models_list.filter(q_obj), search_key


def get_date_dic():
    date_dic = {}
    today_ele = datetime.now().date()

    date_dic['今天'] = today_ele
    date_dic['近七天'] = today_ele - timedelta(days=7)
    date_dic['本月'] = today_ele.replace(day=1)
    date_dic['近一月'] = today_ele - timedelta(days=30)
    date_dic['近90天'] = today_ele - timedelta(days=90)
    date_dic['近180天'] = today_ele - timedelta(days=180)
    date_dic['今年'] = today_ele.replace(month=1, day=1)
    date_dic['近一年'] = today_ele - timedelta(days=365)

    return date_dic