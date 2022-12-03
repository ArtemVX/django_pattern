from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordChangeDoneView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView

from meetups.models import Participant
from meetups.utils import DataMixin
from user.forms import LoginUserForm, RegisterUserForm


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'meetups/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Authentication')
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('meetups')


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'meetups/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Registration')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        Participant.objects.get_or_create(email=form.instance.email)

        return redirect('meetups')


def logout_user(request):
    logout(request)
    return redirect('login')


class Profile(DataMixin, DetailView):
    model = User
    template_name = 'meetups/profile.html'
    pk_url_kwarg = 'user_pk'
    context_object_name = 'selected_user'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        current_user = self.request.user
        c_def = self.get_user_context(title='Your profile', current_user=current_user)

        return dict(list(context.items()) + list(c_def.items()))


class PasswordChange(DataMixin, PasswordChangeView):
    template_name = 'meetups/password-change.html'
    success_url = reverse_lazy('password_change_done')


class PasswordChangeDone(DataMixin, PasswordChangeDoneView):
    template_name = 'meetups/password_change_done.html'