# Generated by Django 5.0.6 on 2024-07-01 17:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task2', '0013_otpmodel_used'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='otpmodel',
            name='used',
        ),
        migrations.AlterUniqueTogether(
            name='groupmembermodel',
            unique_together={('username',)},
        ),
    ]
