from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class MainCategory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    is_default = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name


class SubCategory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    category = models.ForeignKey(MainCategory, on_delete=models.SET_NULL, blank=True, null=True)

    def __unicode__(self):
        return self.name


class Transaction(models.Model):
    TRANSACTION_TYPES = (
        (1, 'Income'),
        (2, 'Expense')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    main_category = models.ForeignKey(MainCategory, on_delete=models.SET_NULL, blank=True, null=True)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, blank=True, null=True)
    transaction_type = models.SmallIntegerField(choices=TRANSACTION_TYPES)
    amount = models.FloatField(default=0.0)
    payee = models.CharField(max_length=500, blank=True, null=True)
    transaction_datetime = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return '{}-{}'.format(self.transaction_type, self.amount)
