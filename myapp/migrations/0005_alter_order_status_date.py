# Generated by Django 4.1.1 on 2022-11-08 02:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_alter_category_options_product_interested_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status_date',
            field=models.DateField(blank=True, max_length=30, null=True),
        ),
    ]