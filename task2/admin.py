from django.contrib import admin

from task2.models import TaskModel, GroupModel, GroupMemberModel, OtpModel


# Register your models here.
admin.site.register(TaskModel)
admin.site.register(GroupModel)
admin.site.register(OtpModel)
admin.site.register(GroupMemberModel)
