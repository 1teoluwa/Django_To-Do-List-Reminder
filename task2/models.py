from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator


# Create your models here.
class TaskModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name= models.TextField(max_length=50)
    email= models.EmailField(max_length=200, default='oludareisaac01@gmail.com')
    task = models.TextField()
    time= models.DateTimeField()


    def __str__(self):
        return self.name


class GroupModel(models.Model):
    name= models.TextField(max_length=50, unique=True)
    group_member_size_limit =  models.IntegerField(default=10, validators=[MaxValueValidator(12)])
    group_task = models.TextField(max_length=50, default='create a task')
    time = models.DateTimeField()

    def save(self, *args, **kwargs):
        self.name = self.name.lower()  # Convert the name to lowercase before saving
        super(GroupModel, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class GroupMemberModel(models.Model):
    group = models.ForeignKey(GroupModel, on_delete=models.CASCADE)
    username = models.TextField(max_length=50)
    user_email= models.TextField(max_length=50)
    # group_id = models.IntegerField()

    class Meta:
        unique_together = ['username']

    def __str__(self):
        return self.user_email


class OtpModel(models.Model):
    otp = models.IntegerField()

    def verify_otp(self, otp):
        if self.otp == otp:
            self.delete()  # Delete the instance upon successful verification
            return True
        return False

    def __str__(self):
        return str(self.otp)
