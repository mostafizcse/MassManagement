# Generated by Django 2.1.2 on 2018-10-26 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messApp', '0013_auto_20181027_0030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
