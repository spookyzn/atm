#coding=utf-8

from django.db import models

#category
class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name="行业名称")
    alias = models.CharField(max_length=32, verbose_name="代号", blank=True)
    comment = models.TextField(blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = u'category'
        verbose_name = "所属行业"

#Type of stock
class StockType(models.Model):
    name = models.CharField(max_length=255, verbose_name="名称")
    alias = models.CharField(max_length=32, verbose_name="代号", blank=True)
    comment = models.TextField(blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = u'stocktype'
        verbose_name = "市场"


#Stock table
class Stock(models.Model):
    sid = models.CharField(max_length=6, primary_key=True, verbose_name="股票代码")
    type = models.ForeignKey(StockType, verbose_name="交易所")
    name = models.CharField(max_length=15, verbose_name="简称")
    category = models.ForeignKey(Category, verbose_name="所属行业")
    full_name = models.CharField(max_length=255, verbose_name="全称", blank=True)
    en_name = models.CharField(max_length=255, verbose_name="英文名称", blank=True)
    address = models.CharField(max_length=512, verbose_name="注册地址", blank=True)
    ipo_date = models.CharField(max_length=32, verbose_name="上市日期")
    state = models.CharField(max_length=64, verbose_name="所属地")
    web = models.CharField(max_length=512, verbose_name="公司网址", blank=True)

    def __unicode__(self):
        return "%s-%s" % (self.sid, self.name)

    class Meta:
        db_table = u'stock'
        verbose_name = "股票"


#Metric data
class Metric(models.Model):
    stock = models.ForeignKey(Stock)
    pos_1 = models.IntegerField(default=0)
    pos_2 = models.IntegerField(default=0)
    pos_3 = models.IntegerField(default=0)
    neg_1 = models.IntegerField(default=0)
    neg_2 = models.IntegerField(default=0)
    neg_3 = models.IntegerField(default=0)
    neutral = models.IntegerField(default=0)
    total = models.IntegerField(default=0)
    focus = models.IntegerField(default=0)
    open_price = models.DecimalField(max_digits=5, decimal_places=2)
    close_price = models.DecimalField(max_digits=5, decimal_places=2)
    high_price = models.DecimalField(max_digits=5, decimal_places=2)
    low_price = models.DecimalField(max_digits=5, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = u'metric'

class Summary(models.Model):
    stock = models.ForeignKey(Stock)
    rate = models.IntegerField(default=0)
    focus = models.IntegerField(default=0)

    class Meta:
        db_table = u'summary'




