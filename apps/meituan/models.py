from django.db import models
from django.contrib.auth import get_user_model
from django.utils.timezone import now
import random

MTUser = get_user_model()


class Merchant(models.Model):
    """
    商家表
    """
    name = models.CharField(max_length=200, verbose_name='商家名称', null=False)
    address = models.CharField(max_length=200, verbose_name='商家', null=False)
    logo = models.CharField(max_length=200, verbose_name='商家logo', null=False)
    notice = models.CharField(max_length=200, verbose_name='商家的公告', null=True, blank=True)
    up_send = models.DecimalField(verbose_name='起送价', default=0, max_digits=6, decimal_places=2)
    lon = models.FloatField(verbose_name='经度')
    lat = models.FloatField(verbose_name='纬度')
    create_time = models.DateTimeField(auto_now=True, null=True)

    created = models.ForeignKey(MTUser, on_delete=models.SET_NULL, null=True)


class GoodsCategory(models.Model):
    """
    商家商品分类
    """
    name = models.CharField(max_length=20, verbose_name='分类名称')
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE, verbose_name='所属商家', related_name='categories')


class Goods(models.Model):
    """
    商品
    """
    name = models.CharField(max_length=200, verbose_name='商品名称')
    picture = models.CharField(max_length=200, verbose_name='商品图片')
    intro = models.CharField(max_length=200)
    price = models.DecimalField(verbose_name='商品价格', max_digits=6, decimal_places=2)  # 最多6位数，2位小数。9999.99
    category = models.ForeignKey(GoodsCategory, on_delete=models.CASCADE, related_name='goods_list')


class UserAddress(models.Model):
    """
    用户的地址
    """
    realname = models.CharField(max_length=100, verbose_name='真是姓名')
    telephone = models.CharField(max_length=11, verbose_name='手机号码')
    province = models.CharField(max_length=100, verbose_name='省份')
    city = models.CharField(max_length=100, verbose_name='城市')
    county = models.CharField(max_length=100, verbose_name='区县')
    address_detail = models.CharField(max_length=100, verbose_name='详细地址')
    area_code = models.CharField(max_length=10, verbose_name='区域代号', null=True)
    is_default = models.BooleanField(default=False, verbose_name='是否是默认地址')
    user = models.ForeignKey(MTUser, related_name='addresses', on_delete=models.CASCADE)


def generate_order_uid():
    # 年   月 日  时 分 秒 四位随机数
    # 2012 04 01 10 23 56 6210
    now_date = now()
    year = str(now_date.year)
    month = str(now_date.month).zfill(2)
    day = str(now_date.day).zfill(2)
    hour = str(now_date.hour).zfill(2)
    minute = str(now_date.minute).zfill(2)
    second = str(now_date.second).zfill(2)
    random_str = str(random.randint(1000, 9999))
    return year + month + day + hour + minute + second + random_str


class Order(models.Model):
    # 支付方式
    PAY_METHOD_CHOICES = (
        (0, '未选择'),
        (1, '微信支付'),
        (2, '支付宝')
    )
    # 订单状态
    ORDER_STATUS_CHOICES = (
        (1, '待支付'),
        (2, '待发货'),
        (3, '配送中'),
        (4, '待评价'),
        (5, '已完成')
    )
    order_id = models.CharField(max_length=100, default=generate_order_uid, verbose_name='订单id', primary_key=True)
    pay_method = models.SmallIntegerField(choices=PAY_METHOD_CHOICES, default=0, verbose_name='支付方式')
    order_status = models.SmallIntegerField(choices=ORDER_STATUS_CHOICES, default=1, verbose_name='订单状态')
    goods_count = models.SmallIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='成交总价')
    goods_list = models.ManyToManyField(Goods)
    user = models.ForeignKey(MTUser, on_delete=models.CASCADE, related_name='orders', verbose_name='用户')
    address = models.ForeignKey(UserAddress, on_delete=models.CASCADE, verbose_name='地址')
