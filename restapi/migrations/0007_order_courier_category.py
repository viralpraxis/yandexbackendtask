# Generated by Django 3.1.7 on 2021-03-20 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restapi', '0006_auto_20210319_1400'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='courier_category',
            field=models.CharField(max_length=25, null=True),
        ),
    ]
