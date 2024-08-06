from task2.forms import TaskForm, JoinGroupForm, CreateGroupForm, VerifyOtpForm
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponse
from .models import TaskModel, GroupModel, GroupMemberModel, OtpModel
from django.shortcuts import render
from django.views.generic import TemplateView
from task2.tasks import send_email_reminder_task, email_otp
from django.http import HttpResponseRedirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib import messages
import random #for otp
import string #for otp
from django.db import IntegrityError
# from celery.schedules import crontab



class JoinGroupView(FormView):
    template_name = 'task2/join_group.html'
    form_class = JoinGroupForm
    success_url = reverse_lazy('verify_otp')  # Redirect to OTP verification page
    proceed = reverse_lazy('chat-room')

    def form_valid(self, form):
        cleaned_data = form.cleaned_data
        group_name = cleaned_data['group_name']
        user_name = cleaned_data['username']
        email = cleaned_data['email']

        # Check if the data already exists in GroupModel
        if self.is_data_duplicate(cleaned_data):
            # Check if the group is full
            group_status = self.is_group_full(cleaned_data)
            if group_status == "Group Is Full":
                form.add_error(None, "The group is full. Please choose another group.")
                return self.form_invalid(form)
            else:
                try:
                    # Data exists, create GroupMemberModel instance
                    group = GroupModel.objects.get(name=group_name)
                    user = GroupMemberModel.objects.create(group_id=group.id, user_email=email, username=user_name)
                    user.save()  # Save the instance

                    otp = self.generate_otp()
                    email_otp.delay(user_name, email, group_name, otp.otp)
                    return redirect(self.success_url)
                except IntegrityError as e:
                    # Handle the integrity error for duplicate username
                    form.add_error('username', 'Username already exists. Please choose another username.')
                    return self.form_invalid(form)
        else:
            # Data does not exist, handle case as needed (e.g., display error message)
            form.add_error(None, "The group does not exist. Please choose a valid group.")
            return self.form_invalid(form)

    def is_group_full(self, cleaned_data):
        group_name = cleaned_data.get('group_name')
        if GroupModel.objects.filter(name=group_name).exists():
            group = GroupModel.objects.get(name=group_name)
            # Assuming group_member_size_limit is the maximum number of members allowed
            member_count = GroupMemberModel.objects.filter(group=group).count()
            if member_count >= group.group_member_size_limit:
                return "Group Is Full"
            return False
        return True  # Return True to indicate the group is full if it doesn't exist

    def is_data_duplicate(self, cleaned_data):
        # Check if the data is already in GroupModel
        group_name = cleaned_data.get('group_name')
        return GroupModel.objects.filter(name=group_name).exists()

    def generate_otp(self, length=6):
        digits = string.digits
        otp_str = ''.join(random.choice(digits) for _ in range(length))
        otp = OtpModel.objects.create(otp=int(otp_str))
        return otp

class TaskList(ListView):
    model = TaskModel
    context_object_name = "tasks"
    template_name = 'task2/tasks.html'
    # form_class = TaskForm

class TaskDetail(DetailView):
    model = TaskModel
    context_object_name = "task"
    template_name = 'task2/review.html'

class ReviewEmailView(CreateView):
    template_name = 'task2/review.html'
    form_class = TaskForm
    model= TaskModel


    def form_valid(self, form):
        form.instance.name = form.cleaned_data['name']
        form.instance.email = form.cleaned_data['email']
        form.instance.review = form.cleaned_data['task']
        form.instance.time = form.cleaned_data['time']
        self.object = form.save()
        form.send_email()
        msg = "Good Job!..... You just added another task"
        self.reminder(form.instance)  # Call reminder method here
        return HttpResponseRedirect(reverse_lazy('task'))


    def reminder(self, task):
        # Calculate the time difference between current time and task time
        current_time = timezone.now()
        time_diff = task.time - current_time
        # Schedule the reminder task to execute at the specified time
        if time_diff.total_seconds() >= 0:
            # Schedule the reminder task to execute at the specified time
            send_email_reminder_task.apply_async(
                args=[task.id],
                countdown=time_diff.total_seconds()
            )
class CreateGroup(CreateView):
    model = GroupModel
    form_class = CreateGroupForm
    # fields = ["name","group_member_size_limit", "group_task", "time"]
    success_url = reverse_lazy('task')

class TaskUpdate(UpdateView):
    model = TaskModel
    form_class = TaskForm
    template_name = 'task2/update.html'
    success_url = reverse_lazy('task')

class DeleteView(DeleteView):
    model = TaskModel
    context_object_name = "task"
    success_url = reverse_lazy('task')


class VerifyOtpView(FormView):
    template_name = 'task2/otp.html'
    form_class = VerifyOtpForm
    success_url = reverse_lazy('chat-room')

    def form_valid(self, form):
        otp = form.cleaned_data['otp']

        try:
            otp_instance = OtpModel.objects.get(otp=otp)

            if otp_instance.verify_otp(otp):
                messages.success(self.request, 'OTP verified successfully!')
                return redirect(self.success_url)
            else:
                messages.error(self.request, 'Incorrect OTP. Please confirm and try again.')
                return self.form_invalid(form)

        except OtpModel.DoesNotExist:
            messages.error(self.request, 'Invalid OTP. Please try again.')
            return self.form_invalid(form)

# class GroupTaskList(ListView):
#     model = JoinGroupModel
#     context_object_name = "group_task"
#     template_name = 'task2/grouptaskview.html'
#     group = JoinGroupForm
#
#     def get_queryset(self):
#         group_name = self.request.GET.get('group_name', None)
#
#         if group_name:
#             print(f"Group name received: {group_name}")  # Debugging line
#             return JoinGroupModel.objects.filter(group_name=group_name).values('user_name')
#         else:
#             print("No group name received")  # Debugging line
#             return JoinGroupModel.objects.none()
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['group_name'] = self.request.GET.get('group_name', '')
#         return context

class LobbyView(TemplateView):
    template_name = 'task2/lobby.html'
    model = GroupMemberModel
    context_object_name = "group_members"