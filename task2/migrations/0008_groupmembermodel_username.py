# Generated by Django 5.0.6 on 2024-06-27 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task2', '0007_otpmodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupmembermodel',
            name='username',
            field=models.TextField(default='Iteoluwa', max_length=50),
        ),
    ]
