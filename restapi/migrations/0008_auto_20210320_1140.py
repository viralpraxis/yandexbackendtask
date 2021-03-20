# Generated by Django 3.1.7 on 2021-03-20 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restapi', '0007_order_courier_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courier',
            name='category',
            field=models.CharField(choices=[('foot', 'Foot'), ('bike', 'Bike'), ('car', 'Car')], max_length=10),
        ),
    ]
