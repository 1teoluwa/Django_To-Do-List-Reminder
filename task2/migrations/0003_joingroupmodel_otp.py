# Generated by Django 5.0.6 on 2024-06-20 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task2', '0002_alter_joingroupmodel_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='joingroupmodel',
            name='otp',
            field=models.IntegerField(default=123456, max_length=6),
        ),
    ]