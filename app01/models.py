from django.db import models

# Create your models here.
class Department(models.Model):
    """部门表"""
    title = models.CharField(verbose_name="标题",max_length=32)
    def __str__(self):
        return self.title

class UserInfo(models.Model):
    """员工表"""
    name = models.CharField(verbose_name="姓名",max_length=16)
    password = models.CharField(verbose_name="密码",max_length=64)
    age = models.IntegerField(verbose_name="年龄")
    account = models.DecimalField(verbose_name="账户余额",max_digits=10,decimal_places=2,default=0)
    create_time = models.DateTimeField(verbose_name="入职时间")
    # 有约束 cascade表示级联删除
    depart = models.ForeignKey(verbose_name="部门",to="Department",to_field="id",on_delete=models.CASCADE)
    gender_choices = (
        (1,"男"),
        (2,"女"),
    )
    gender = models.SmallIntegerField(verbose_name="性别",choices=gender_choices)

    def __str__(self):
        return self.name

class PrettyNum(models.Model):
    """靓号表"""
    mobile = models.CharField(verbose_name="手机号",max_length=11)
    price = models.IntegerField(verbose_name="价格",default=0)
    level_choices = (
        (1,"1级"),
        (2,"2级"),
        (3,"3级"),
        (4,"4级"),
    )
    level = models.SmallIntegerField(verbose_name="级别",choices=level_choices,default=1)
    status_choices = (
        (1,"已占用"),
        (2,"未占用"),
    )
    status = models.SmallIntegerField(verbose_name="状态",choices=status_choices,default=2)


class Admin(models.Model):
    """管理员"""
    username = models.CharField(verbose_name="用户名",max_length=32)
    password = models.CharField(verbose_name="密码",max_length=64)
    level_choices = (
        (1,"超级"),
        (2,"普通"),
    )
    level = models.SmallIntegerField(verbose_name="级别", choices=level_choices, default=2)

class Order(models.Model):
    """订单"""
    oid = models.CharField(verbose_name="订单号",max_length=64)
    title = models.CharField(verbose_name="名称",max_length=32)
    price = models.IntegerField(verbose_name="价格")
    status_choices = (
        (1,"待支付"),
        (2,"已支付"),
    )
    status = models.SmallIntegerField(verbose_name="订单状态",choices=status_choices,default=1)
    username = models.ForeignKey(verbose_name="用户",to="UserInfo",to_field="id",on_delete=models.CASCADE)


class City(models.Model):
    name = models.CharField(verbose_name="名称",max_length=32)
    count = models.IntegerField(verbose_name="人口",default=0)
    img = models.FileField(verbose_name="Logo",max_length=128,upload_to="city/")
