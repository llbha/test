# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Chaojiying(models.Model):
    img = models.CharField(max_length=255, blank=True, null=True)
    pic_str = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'chaojiying'


class Company(models.Model):
    credit_code = models.CharField(max_length=255, blank=True, null=True)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    types = models.CharField(max_length=255, blank=True, null=True)
    legal_person = models.CharField(max_length=255, blank=True, null=True)
    reg_capital = models.CharField(max_length=255, blank=True, null=True)
    register_date = models.CharField(max_length=255, blank=True, null=True)
    bengin_time = models.CharField(max_length=255, blank=True, null=True)
    end_time = models.CharField(max_length=255, blank=True, null=True)
    reg_auth = models.CharField(max_length=255, blank=True, null=True)
    approver_date = models.CharField(max_length=255, blank=True, null=True)
    reg_status = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    business_scope = models.CharField(max_length=255, blank=True, null=True)
    unit = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'company'


##[jetbrains/home/ubuntu/company/enterprise/models.py,/home/ubuntu/company/enterprise/__pycache__/models.cpython-36.pyc
