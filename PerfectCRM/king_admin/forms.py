from django import forms


def create_model_form(request,admin_class):
    '''动态生成Model Form'''

    # 修改样式
    def __new__(cls, *args, **kwargs):
        #print(cls.base_fields)     OrderedDict([('name', <django.forms.fields.CharField object at 0x000001385625DA90>)]),
        for field_name,field_obj in cls.base_fields.items():
            # 根据 cls.base_field 的特性给每个字段加上样式
            cls.base_fields[field_name].widget.attrs['class'] = 'form-control'

        return forms.ModelForm.__new__(cls)

    class Meta:
        model = admin_class.model        # 通过admin_class动态获取model
        # fields = ('name', 'qq')        # 可以获取指定字段
        # age = forms.IntegerField()     # 还可以添加字段
        fields = '__all__'               # '__all__'获取所有字段

    attrs = {'Meta':Meta}

    _model_form_class = type("DynamicModelForm", (forms.ModelForm,), attrs)     # 第一个参数是类名，第二个参数是元组，填写父类，最后必须添加逗号，

    # 方法一定要 setattr                                                                       #  第三个参数字典形式的Meta类
    setattr(_model_form_class,'__new__',__new__)

    return _model_form_class    # 返回的是一个类