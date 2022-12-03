from django.contrib.auth import logout, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User, AbstractUser
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordChangeDoneView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

from .models import MeetUp, Participant
from .forms import NewMeetupForm
from .utils import *



class MeetupHome(DataMixin, ListView):
    model = MeetUp  # model
    template_name = 'meetups/index.html'  # path to the template
    context_object_name = 'meetups'  # name to add data from model into template
    paginate_by = 3  # max number of objects

    # add extra data(context)
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Home page")  # без Mixin -> context["title"] = 'Home page'
        return dict(list(context.items()) + list(c_def.items()))

    # filter to get data from model
    def get_queryset(self):
        return MeetUp.objects.filter(date='2022-11-29')


# def index(request):  # any name
#     meetups = MeetUp.objects.all()
#     return render(request, 'meetups/index.html', {'meetups': meetups})


class MeetupDetails(DataMixin, DetailView):
    model = MeetUp
    template_name = 'meetups/meetup-details.html'
    context_object_name = 'selected_meetup'
    slug_url_kwarg = 'meetup_slug'  # or pk_url_kwarg

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=str(context['selected_meetup'].slug),
                                      meetup_found=True)
        return dict(list(context.items()) + list(c_def.items()))


# def meetup_details(request, meetup_slug):
#     try:
#         selected_meetup = MeetUp.objects.get(slug=meetup_slug)
#
#         if request == 'GET':
#             registration_form = NewVisitorForm()
#         else:
#             registration_form = NewVisitorForm(request.POST)
#             if registration_form.is_valid():
#                 user_email = registration_form.cleaned_data['email']
#                 participant, _ = Participant.objects.get_or_creat(email=user_email)
#                 selected_meetup.participants.add(participant)
#                 return redirect('confirm-registration', meetup_slug=meetup_slug)
#
#         return render(request, 'meetups/meetup-details.html', dict(selected_meetup=selected_meetup,
#                                                                    form=registration_form,
#                                                                    meetup_found=True))
#     except MeetUp.DoesNotExist:
#         return render(request, 'meetups/meetup-details.html', dict(meetup_found=False,
#                                                                    error_message='No such meet up'))


def confirm_registration(request, meetup_slug):
    if request.user.is_authenticated:
        selected_meetup = MeetUp.objects.get(slug=meetup_slug)
        participant, _ = Participant.objects.get_or_create(email=request.user.email)
        selected_meetup.participants.add(participant)
        return render(request, 'meetups/registration-success.html', dict(organizer=selected_meetup.organizer_email))
    else:
        return redirect('login')


class NewMeetup(LoginRequiredMixin, DataMixin, CreateView):  # LoginRequiredMixin for functions is @login_required
    form_class = NewMeetupForm
    template_name = 'meetups/new-meetup.html'
    # success_url = reverse_lazy('meetup-detail')   # if get_absolute_url() in model, reverse is automatically

    # for LoginRequiredMixin
    login_url = reverse_lazy('home')  # if not Login reverse to another page
    raise_exception = True  # if not Login raise 403 ex

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='New meetup')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        form.instance.organizer_email = self.request.user.email
        form.save()
        return super().form_valid(form)


# def new_meetup(request):
#     if request.method == 'POST':
#         form = NewMeetupForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('meetups')
#     else:
#         form = NewMeetupForm()
#
#     return render(request, 'meetups/new-meetup.html', {'form': form})



# def profile(request, username):
#     return render(request, 'meetups/profile.html', {'username': username})
