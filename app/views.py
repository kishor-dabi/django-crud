from django.shortcuts import render, redirect, get_object_or_404

from app.forms import UserForm, UserProfileInfoForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import LoginForm
from django.contrib.auth.models import User
from django.views.generic import FormView, RedirectView, ListView, DetailView
from django.views.generic.edit import UpdateView
from .models import UserProfileInfo
# import logging
#
# l = logging.getLogger('django.db.backends')
# l.setLevel(logging.DEBUG)
# l.addHandler(logging.StreamHandler())
# Create your views here.


@login_required
def index(request):
    print('-----------------')
    return render(request, 'app/index.html')


@login_required
def special(request):
    return HttpResponse("You are logged in !")


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.email = user.username;
            user.set_password(user.password)
            print(user)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            # if 'profile_pic' in request.FILES:
            #     print('found it')
            #     profile.profile_pic = request.FILES['profile_pic']
            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        # profile_form = UserProfileInfoForm()
        attrs = {'class': 'form-control'}
    return render(request, 'app/register.html',
                          {'user_form': user_form,
                           # 'profile_form': profile_form,
                           'registered': registered})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Your account was inactive.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details given")
    else:
        return render(request, 'app/login.html', {})


class UserLogin(FormView):

    form_class = LoginForm
    template_name = 'app/login.html'

    # def get(self, request):
    #     form = self.form_class(None)
    #     return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        username = request.POST.get('email')
        password = request.POST.get('password')
        print(username, password)

        if form.is_valid():

            # storing the data but NOT SAVING them to db yet
            user = form.save(commit=False)

            # if credentials are correct, this returns a user object
            user = authenticate(username=username, password=password)
            print(form, '----------', user)

            if user is not None:

                if user.is_active:
                    login(request, user)
                    return redirect('index')
            else:

                messages.error(request, "Enter valid email and password")
        print(form, user)
        return redirect('app:user_login')

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})


class Dashboard(ListView):
    model = User
    template_name = 'app/dashboard.html'

    def get(self, request):
        users = User.objects.all()
        print(users.count(), "--------", users.values())
        response_data = {"users": users}
        if users.count() == 0:
            user_message = "No record Found"
            response_data['message'] = user_message

        return render(request, self.template_name, response_data)


class ProfileView(UpdateView):
    model = User
    template_name = 'app/my_profile.html'
    object = None

    user_form = UserProfileForm()
    profile_image_form = UserProfileInfoForm()

    def get(self, request, **kwargs):

        print(request.session.get('_auth_user_id'))
        user = get_object_or_404(User, pk=request.session.get('_auth_user_id'))
        userProfile = get_object_or_404(UserProfileInfo, user_id=request.session.get('_auth_user_id'))
        # user = User.objects.filter(pk=request.session.get('_auth_user_id'))
        # print(self.user_form, profile_image_form)
        response_data = {"users": request.session}
        # if users.count() == 0:
        #     user_message = "No record Found"
        #     response_data['message'] = user_message
        print(request.session.get('_auth_user_id'), user)
        user_form = UserProfileForm(instance=user)
        profile_image_form = UserProfileInfoForm(instance=userProfile)
        # return self.render_to_response(self.get_context_data(
        #     object=self.object, user_form=user_form, profile_image_form=profile_image_form))

        return render(request, self.template_name, {'user_form': user_form, 'profile_image_form': profile_image_form})

    def post(self, request):
        # user_form = UserProfileForm(data=request.POST)
        profile_form = UserProfileInfoForm(request.POST)
        print(profile_form.is_valid(), profile_form)
        if profile_form.is_valid():
            # user = user_form.save(commit=False)
            # user['id'] = request.session.get('_auth_user_id')
            # user.set_password(user.password)
            # print(user, "------------------------------")
            # user.update()
            # profile.user = request.user#.get('_auth_user_id')
            # user = get_object_or_404(User, pk=request.session.get('_auth_user_id'))
            # print(profile_form)

            profile = profile_form.save(commit=False)
            # profile.user_id = request.user
            profileObj = get_object_or_404(UserProfileInfo, user_id=request.session.get('_auth_user_id'))
            profile.user_id = request.session.get('_auth_user_id')
            profile.id = profileObj.id
            print(profile, "+++++++++++++++++++++++++++++++")
            if 'profile_pic' in request.FILES:
                print('found it')
                profile.profile_pic = request.FILES['profile_pic']
            profile.save()
            return render(request, self.template_name, {'messages': "Update Successfully", "isUpdate": True})
        else:
            return render(request, self.template_name, {'user_form': self.user_form,
                                                        'profile_image_form': self.profile_image_form,
                                                        'messages': "Please fill all fields", "isUpdate": False})
