# Generated by Django 5.0.6 on 2024-06-27 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task2', '0005_groupmembermodel_delete_joingroupmodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupmembermodel',
            name='group_id',
            field=models.IntegerField(),
        ),
    ]
