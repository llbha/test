# Generated by Django 2.2.3 on 2019-07-05 06:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('credit_code', models.CharField(max_length=255, verbose_name='统一社会信用代码')),
                ('company_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='企业名称')),
                ('types', models.CharField(blank=True, max_length=255, null=True, verbose_name='类型')),
                ('legal_person', models.CharField(blank=True, max_length=255, null=True, verbose_name='法定代表人')),
                ('reg_capital', models.CharField(blank=True, max_length=255, null=True, verbose_name='注册资本')),
                ('register_date', models.CharField(blank=True, max_length=255, null=True, verbose_name='成立日期')),
                ('bengin_time', models.CharField(blank=True, max_length=255, null=True, verbose_name='营业期限自')),
                ('end_time', models.CharField(blank=True, max_length=255, null=True, verbose_name='营业期限至')),
                ('reg_auth', models.CharField(blank=True, max_length=255, null=True, verbose_name='登记机关')),
                ('approver_date', models.CharField(blank=True, max_length=255, null=True, verbose_name='核准日期')),
                ('reg_status', models.CharField(blank=True, max_length=255, null=True, verbose_name='登记状态')),
                ('address', models.CharField(blank=True, max_length=255, null=True, verbose_name='住所')),
                ('business_scope', models.CharField(blank=True, max_length=255, null=True, verbose_name='经营范围')),
                ('unit', models.CharField(blank=True, max_length=255, null=True, verbose_name='对应企业名称')),
            ],
            options={
                'verbose_name': '企业工商信息',
                'verbose_name_plural': '企业工商信息',
                'db_table': 'company',
                'managed': False,
            },
        ),
    ]