from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Customer(models.Model):
    '''客户信息表'''
    name = models.CharField(max_length=32, blank=True, null=True)

    # 名义上为qq，可以填写别的联系方式
    qq = models.CharField(max_length=64, unique=True)
    qq_name = models.CharField(max_length=64, blank=True, null=True)
    phone = models.CharField(max_length=64, blank=True, null=True)

    source_choices = (
        (0, '转介绍'),
        (1, 'QQ群'),
        (2, '官网'),
        (3, '百度推广'),
        (4, '51CTO'),
        (5, '知乎'),
        (6, '市场推广'),
    )

    # small两个字节，节省空间

    source = models.SmallIntegerField(choices=source_choices)
    # 介绍人信息 ,verbose (详细)
    referral_from = models.CharField(verbose_name='转介绍人qq', max_length=64, blank=True, null=True)

    # 咨询课程
    consult_course = models.ForeignKey('Course',on_delete=models.CASCADE,verbose_name='咨询课程')
    content = models.TextField(verbose_name='咨询详情')
    # 顾问
    consultant = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
    # 备注
    memo = models.TextField(blank=True, null=True)

    # add 与没用add的区别
    date = models.DateTimeField(auto_now_add=True)

    tags = models.ManyToManyField('Tag')

    def __str__(self):
        return self.qq

    class Meta:
        verbose_name_plural = '客户信息'


class Tag(models.Model):
    name = models.CharField(unique=True, max_length=32)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = '标签'


class CustomerFollowUp(models.Model):
    '''客户跟进表'''
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    content = models.TextField(verbose_name='跟进内容')
    # 跟进人
    consultant = models.ForeignKey('UserProfile', on_delete=models.CASCADE)

    date = models.DateTimeField(auto_now_add=True)

    #报名意向
    intantion_choices = (
        (0,'一星期内报名'),
        (1,'一个月内报名'),
        (2,'近期内无报名意向'),
        (3,'已在其它机构报名'),
        (4,'已报名'),
    )

    intantion = models.SmallIntegerField(choices=intantion_choices)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '<%s: %s>'%(self.customer.qq, self.intantion)

    class Meta:
        verbose_name_plural = '客户跟进状况'


class Course(models.Model):
    '''课程表'''
    name = models.CharField(max_length=64, unique=True)
    # Positive 正数
    price = models.PositiveSmallIntegerField()
    # 周期
    period = models.PositiveSmallIntegerField(verbose_name='周期(月)')
    # 课程大纲
    outline = models.TextField()

    def __str__(self):
        return self.name

    # class Meta:
    #     verbose_name_plural = '课程'


class Branch(models.Model):
    '''校区表'''
    name = models.CharField(max_length=64,unique=True)
    addr = models.CharField(max_length=64)

    def __str__(self):
        return self.name

    # class Meta:
    #     verbose_name_plural = '校区'


class ClassList(models.Model):
    '''班级表'''
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    teachers = models.ManyToManyField('UserProfile')
    # 第几期
    semester = models.PositiveSmallIntegerField()
    # 分校校区
    branch = models.ForeignKey('Branch', on_delete=models.CASCADE)
    start_date= models.DateField('开班日期')
    end_date = models.DateField(verbose_name='结业日期', blank=True, null=True)

    class_type_choices = (
        (0,'面授(全期)'),
        (1,'面授(周末)'),
        (2,'网络班'),
    )
    class_type = models.SmallIntegerField(choices=class_type_choices, verbose_name='班级类型')

    def __str__(self):
        return '%s %s %s'.format(self.branch, self.semester, self.course)

    # 班级应该唯一，但是不同校区可能有同样的名字，所以需要 “联和” 唯一
    class Meta:
        unique_together = ('branch','semester','course')
        # verbose_name_plural = '班级'


class CourseRecord(models.Model):
    '''上课记录'''
    from_class = models.ForeignKey('ClassList', on_delete=models.CASCADE)
    teacher = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
    day_num = models.PositiveSmallIntegerField(verbose_name='第几节(天)')
    has_homework = models.BooleanField(default=True)
    homework_title = models.CharField(max_length=64, blank=True, null=True)
    homework_content = models.TextField(blank=True, null=True)
    outline = models.TextField(verbose_name='课程大纲')
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return '%s %s'.format(self.from_class, self.day_num)

    class Meta:
        unique_together = ('from_class', 'day_num')
        # verbose_name_plural = '上课记录'


class StudyRecord(models.Model):
    '''学习记录'''
    student = models.ForeignKey('Enrollment', on_delete=models.CASCADE)
    course_record = models.ForeignKey('CourseRecord', on_delete=models.CASCADE)
    # 出勤
    attendance_choices = (
        (0,'已签到'),
        (1,'迟到'),
        (2,'缺勤'),
        (3,'早退'),
    )
    attendance = models.SmallIntegerField(choices=attendance_choices, default=0, verbose_name='出勤')

    score_choices = (
        (100,'A+'),
        (90,'A'),
        (85,'B+'),
        (80,'B'),
        (75,'B-'),
        (70,'C+'),
        (60,'C'),
        (40,'C-'),
        (0,'D'),
    )
    score = models.SmallIntegerField(choices=score_choices)

    # 备注
    memo = models.TextField(blank=True, null=True)
    date = models.DateField(auto_now_add=True)

    # class Meta:
    #     verbose_name_plural = '学习记录'


class Enrollment(models.Model):
    '''报名表'''
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    enrolled_class = models.ForeignKey('ClassList', verbose_name='报名班级', on_delete=models.CASCADE)
    consultant = models.ForeignKey('UserProfile', verbose_name='课程顾问', on_delete=models.CASCADE)
    # 合同签署
    contract_agreed = models.BooleanField(default=False, verbose_name='学员合同已签署')
    contract_approved = models.BooleanField(default=False, verbose_name='合同已审核')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s %s'.format(self.customer, self.enrolled_class)

    class Meta:
        unique_together = ('customer', 'enrolled_class')
        # verbose_name_plural = '报名表'


class Payment(models.Model):
    '''消费记录'''
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    course = models.ForeignKey('Course', verbose_name='所报课程', on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(verbose_name='数额', default=500)
    consultant = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = '消费记录'


class Role(models.Model):
    """角色表"""
    name = models.CharField(max_length=32, unique=True)
    menus = models.ManyToManyField('Menu')
    def __str__(self):
        return self.name

    # class Meta:
    #     verbose_name_plural = '角色'


class UserProfile(models.Model):
    '''账号表'''
    # 继承django自带的表进行账号加密处理，
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=32)
    roles = models.ManyToManyField('Role')

    def __str__(self):
        return self.name

    # class Meta:
    #     verbose_name_plural = '账号'


class Menu(models.Model):
    '''菜单 (不同的角色显示不同的菜单)'''
    name = models.CharField(max_length=64)
    url_name = models.CharField(max_length=64, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = '菜单'