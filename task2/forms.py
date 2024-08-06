from django import forms
from task2.tasks import send_review_email_task, send_email_reminder_task, email_otp
from .models import TaskModel, GroupModel, OtpModel

class TaskForm(forms.ModelForm):
    class Meta:
        model = TaskModel
        fields = ['name', 'email', 'task', 'time']

    name = forms.CharField(
        label='Firstname', min_length=4, max_length=50, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Firstname', 'id': 'form-firstname'}))
    task = forms.CharField(
        label="Task", widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '5', 'id': 'form-review'}))
    email = forms.EmailField(
        max_length=200, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'E-mail', 'id': 'form-email'}))
    time = forms.DateTimeField(
        label="Set Alarm",
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'})
    )

    def send_email(self):
        send_review_email_task.delay(
            # data the user typed is used in communicating
            self.cleaned_data['name'], self.cleaned_data['email'], self.cleaned_data['task'], self.cleaned_data['time'])


class JoinGroupForm(forms.ModelForm):
    class Meta:
        model = GroupModel
        fields = ['group_name',"email"]

    username = forms.CharField(
        label='Username', min_length=4, max_length=50, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Username', 'id': 'form-user-name'}))
    group_name = forms.CharField(
            label='Group Name', min_length=4, max_length=50, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Group Name', 'id': 'form-group-name'}))
    email = forms.EmailField(
        max_length=200, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'E-mail', 'id': 'form-email'}))



class CreateGroupForm(forms.ModelForm):
    class Meta:
        model = GroupModel
        fields = ['name', 'group_member_size_limit', 'group_task', 'time']

    name = forms.CharField(
        label='Firstname', min_length=4, max_length=50, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Firstname', 'id': 'form-firstname'}))
    group_member_size_limit = forms.IntegerField(
        min_value= 0, max_value= 12, widget=forms.NumberInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'maximum members are 12', 'id': 'form-group-size'}))
    group_task = forms.CharField(
        label="Task", widget=forms.Textarea(attrs={'placeholder': 'Enter group task','class': 'form-control', 'rows': '5', 'id': 'form-review'}))
    time = forms.DateTimeField(
        label="Set Alarm",
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'})
    )

class VerifyOtpForm(forms.ModelForm):
    class Meta:
        model = OtpModel
        fields = ['otp']

    otp = forms.IntegerField(
            label='OTP', widget=forms.NumberInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Enter One Time Password', 'id': 'form-group-name'}))
