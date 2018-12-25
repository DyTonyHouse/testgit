from django import template
from django.utils.safestring import mark_safe
from king_admin import utils

register = template.Library()


@register.simple_tag
def render_table_name(admin_class):
    return admin_class.model._meta.verbose_name_plural


# @register.simple_tag
# def get_objects_all(admin_class):
#     return admin_class.model.objects.all


@register.simple_tag
def build_table_row(request, model_obj, admin_class):
    row_ele = ''
    ## 如果有字段是 choice 那么该方法得到的是序号，不会显示具体内容，看下面的方法实现
    # for colunm in admin_class.list_display:
    #     colunm_data = getattr(model_obj, colunm)
    #     row_ele += '<td>%s</td>' % colunm_data


    for num,field in enumerate(admin_class.list_display):
        # _meta.get_field(colunm)得到的是该字段的对象
        field_obj = model_obj._meta.get_field(field)
        # 如果这个对象有choices属性，就可以调用 get_column_display 方法获取序号对应的内容
        # ！注意：get_column_display是一个方法，使用getattr后得到的是方法名所以需要在后面加一对括号
        if field_obj.choices:

            # 'get_field_display' 是一个方法，获取字段的值，所以需要加上()调用
            field_data = getattr(model_obj, 'get_%s_display'%field)()

        else:
            # <class 'str'>
            # <class 'datetime.datetime'>
            field_data = getattr(model_obj, field)

            # 使用type后才能调用该对象的__name__方法
        if type(field_data).__name__ == 'datetime':
            field_data = field_data.strftime('%Y-%m-%d %H:%M:%S')

        if num == 0:
            field_data = "<a href='%s%s/change'>%s</a>"%(request.path, model_obj.id, field_data)
        row_ele += '<td>%s</td>' % field_data
    return mark_safe(row_ele)


@register.simple_tag
def loop_display_page(posts, filter_conditions, orderby_key, search_key):
    fil = ''
    ele = ''
    o = ''      # 确保排序后还能翻页
    _q = ''
    flag = False

    if orderby_key:
        o='&%s=%s'%('o', orderby_key)

    if search_key:
        _q = '&%s=%s'%('_q', search_key)

    for k ,v in filter_conditions.items():
        fil += '&%s=%s'%(k,v)

    for page_num in posts.paginator.page_range:
        if page_num < 3 or page_num > posts.paginator.num_pages-2 or abs(posts.number - page_num) <=1:
            cls =''
            if page_num == posts.number:
                flag = False
                cls = 'active'
            ele += '<li class="%s"><a href="?page=%s%s%s%s">%s</a></li>'%(cls, page_num, fil, o, _q, page_num)

        elif flag == False:
            ele += '<li><a>··</a></li>'
            flag = True

    return mark_safe(ele)


@register.simple_tag
def head_page(posts,filter_conditions,orderby_key, search_key):
    fil = ''
    o = ''
    _q = ''
    if orderby_key:
        o = '&%s=%s'%('o', orderby_key)

    if search_key:
        _q = '&%s=%s'%('_q', search_key)

    for k, v in filter_conditions.items():
        if v:
            fil += '&%s=%s' % (k, v)
    return mark_safe('<li><a href="?page=%d%s%s%s">首页</a></li><li><a href="?page=%s%s%s%s">上一页</a></li>'%(1, fil, o, _q, posts.previous_page_number(), fil, o, _q))


@register.simple_tag
def foot_page(posts,filter_conditions, orderby_key, search_key):
    fil = ''
    o = ''
    _q = ''
    if orderby_key:
        o = '&%s=%s'%('o', orderby_key)

    if search_key:
        _q = '&%s=%s'%('_q', search_key)

    for k,v in filter_conditions.items():
        if v:
            fil += '&%s=%s'%(k,v)
    return mark_safe('<li><a href="?page=%s%s%s%s">下一页</a></li><li><a href="?page=%s%s%s%s">尾页</a></li>'%(posts.next_page_number(), fil, o, _q, posts.paginator.num_pages, fil, o, _q))


@register.simple_tag
def render_filter_column(filter_field,admin_class,filter_conditions):
    '''过滤数据'''

    select_ele = "<select class='form-control' name='{filter_field}'><option value=''>---</option>"
    field_obj = admin_class.model._meta.get_field(filter_field)

    if field_obj.choices:
        # print(field_obj.choices)   #((0, '转介绍'), (1, 'QQ群'), (2, '官网'), (3, '百度推广')....)
        for column_content in field_obj.choices:
            selected = ''

            if filter_conditions.get(filter_field) == str(column_content[0]):
                selected = 'selected'

            select_ele += "<option value=%s %s>%s</option>"%(column_content[0],selected, column_content[1])

    if type(field_obj).__name__ == 'ForeignKey':

        # print(field_obj.get_choices())   #[('', '---------'), (1, '销售1号'), (2, '销售2号'), (3, '销售3号')]
        for column_content in field_obj.get_choices()[1:]:
            selected = ''
            if filter_conditions.get(filter_field) == str(column_content[0]):
                selected = 'selected'

            select_ele += "<option value=%s %s>%s</option>"%(column_content[0], selected, column_content[1])

    if type(field_obj).__name__ in 'DateTimeField':

        filter_field_item = "%s__gte" % filter_field

        date_dic = utils.get_date_dic()

        for k,v in date_dic.items():
            selected = ''
            if filter_conditions.get(filter_field_item) == str(v):
                selected = 'selected'
            select_ele += "<option value=%s %s>%s</option>"%(v, selected, k)
    else:
        filter_field_item = filter_field

    select_ele += "</select>"
    select_ele = select_ele.format(filter_field=filter_field_item)

    return mark_safe(select_ele)


@register.simple_tag
def table_header_column_sort(column, orderby_key,filter_condtions):
    ele = ''
    o = ''  # 保存orderby_key 最终的值
    item = ''   # 保证在检索后还能进行排序，不加item检索条件就莫得了

    for k,v in filter_condtions.items():
        if v:
            item += '&%s=%s'%(k,v)

    if orderby_key:
        if '-' in orderby_key:
            o = orderby_key.strip('-')      # strip只能删除字符串的头尾字符，默认删除空格与换行
        else:
            o = '-%s'%orderby_key

    if orderby_key and orderby_key.strip('-') == column:
        ele +='<th><a href="?o=%s%s">%s</a></th>'%(o, item, column)
    else:
        ele += '<th><a href="?o=%s%s">%s</a></th>'%(column, item, column)
    return mark_safe(ele)

@register.simple_tag
def get_field_obj_list(field, admin_class, form_obj):
    '''返回所有待选数据'''

    # 表结构对象的某个字段
    field_obj = getattr(admin_class.model, field.name)
    # 包括了所有的数据
    all_obj_list = field_obj.rel.model.objects.all()
    # all_obj_list = field_obj.objects.all()


    # 单条数据的对象中的某个字段
    if form_obj.instance.id:
        obj_instance_field = getattr(form_obj.instance, field.name)
        selected_obj_list = obj_instance_field.all()
    else:
        # 创建单条数据时直接返回所有数据，因为创建新的数据没有传入 instance
        return all_obj_list
    # 把不在单条数据的的数据存入待选列表中
    standby_obj_list = []
    for obj in all_obj_list:
        if obj not in selected_obj_list:
            standby_obj_list.append(obj)

    return standby_obj_list


@register.simple_tag
def get_field_selected_obj_list(field, form_obj):
    '''返回已选择的数据'''
    if form_obj.instance.id:
        obj_instance_field = getattr(form_obj.instance, field.name)
        selected_obj_list = obj_instance_field.all()
        return selected_obj_list
    # else:
    #     return []


@register.simple_tag
def display_obj_related(model_obj):
    # model_obj = [model_obj,]

    if model_obj:
        model_class = model_obj._meta.model
        model_name = model_obj._meta.model_name


