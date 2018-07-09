"""
Views which allow users to create and activate accounts.

"""

from django.conf import settings
from django.shortcuts import redirect, render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from home.models import Friend
from registration.forms import ResendActivationForm
from django.contrib.auth.models import User
from .forms import UserForm, ProfileForm, CustomRegistrationForm

REGISTRATION_FORM_PATH = getattr(settings, 'REGISTRATION_FORM',
                                 'registration.forms.RegistrationForm')
REGISTRATION_FORM = CustomRegistrationForm
ACCOUNT_AUTHENTICATED_REGISTRATION_REDIRECTS = getattr(
    settings, 'ACCOUNT_AUTHENTICATED_REGISTRATION_REDIRECTS', True)


class RegistrationView(FormView):
    """
    Base class for user registration views.

    """
    disallowed_url = 'registration_disallowed'
    form_class = REGISTRATION_FORM
    http_method_names = ['get', 'post', 'head', 'options', 'trace']
    success_url = None
    template_name = 'registration/registration_form.html'

    @method_decorator(sensitive_post_parameters('password1', 'password2'))
    def dispatch(self, request, *args, **kwargs):
        """
        Check that user signup is allowed and if user is logged in before even borthering to
        dispatch or do other processing.

        """
        if ACCOUNT_AUTHENTICATED_REGISTRATION_REDIRECTS:
            if self.request.user.is_authenticated:
                if settings.LOGIN_REDIRECT_URL is not None:
                    return redirect(settings.LOGIN_REDIRECT_URL)
                else:
                    raise Exception((
                        'You must set a URL with LOGIN_REDIRECT_URL in '
                        'settings.py or set '
                        'ACCOUNT_AUTHENTICATED_REGISTRATION_REDIRECTS=False'))

        if not self.registration_allowed():
            return redirect(self.disallowed_url)
        return super(RegistrationView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        new_user = self.register(form)
        success_url = self.get_success_url(new_user)

        # success_url may be a simple string, or a tuple providing the
        # full argument set for redirect(). Attempting to unpack it
        # tells us which one it is.
        try:
            to, args, kwargs = success_url
        except ValueError:
            return redirect(success_url)
        else:
            return redirect(to, *args, **kwargs)

    def registration_allowed(self):
        """
        Override this to enable/disable user registration, either
        globally or on a per-request basis.

        """
        return True

    def register(self, form):
        """
        Implement user-registration logic here.

        """
        raise NotImplementedError

    def get_success_url(self, user=None):
        """
        Use the new user when constructing success_url.

        """
        return super(RegistrationView, self).get_success_url()


class ActivationView(TemplateView):
    """
    Base class for user activation views.

    """
    http_method_names = ['get']
    template_name = 'registration/activate.html'

    def get(self, request, *args, **kwargs):
        activated_user = self.activate(*args, **kwargs)
        if activated_user:
            success_url = self.get_success_url(activated_user)
            try:
                to, args, kwargs = success_url
            except ValueError:
                return redirect(success_url)
            else:
                return redirect(to, *args, **kwargs)
        return super(ActivationView, self).get(request, *args, **kwargs)

    def activate(self, *args, **kwargs):
        """
        Implement account-activation logic here.

        """
        raise NotImplementedError

    def get_success_url(self, user):
        raise NotImplementedError


class ResendActivationView(FormView):
    """
    Base class for resending activation views.
    """
    form_class = ResendActivationForm
    template_name = 'registration/resend_activation_form.html'

    def form_valid(self, form):
        """
        Regardless if resend_activation is successful, display the same
        confirmation template.

        """
        self.resend_activation(form)
        return self.render_form_submitted_template(form)

    def resend_activation(self, form):
        """
        Implement resend activation key logic here.
        """
        raise NotImplementedError

    def render_form_submitted_template(self, form):
        """
        Implement rendering of confirmation template here.

        """
        raise NotImplementedError


class ApprovalView(TemplateView):

    http_method_names = ['get']
    template_name = 'registration/admin_approve.html'

    def get(self, request, *args, **kwargs):
        approved_user = self.approve(*args, **kwargs)
        if approved_user:
            success_url = self.get_success_url(approved_user)
            try:
                to, args, kwargs = success_url
            except ValueError:
                return redirect(success_url)
            else:
                return redirect(to, *args, **kwargs)
        return super(ApprovalView, self).get(request, *args, **kwargs)

    def approve(self, *args, **kwargs):
        """
        Implement admin-approval logic here.

        """
        raise NotImplementedError

    def get_success_url(self, user):
        raise NotImplementedError


def view_profile(request, username=None):
    current_user = User.objects.get(username=username)
    # to get request.user following
    friend, created = Friend.objects.get_or_create(current_user=request.user)
    following_request_user = friend.friend_list.all()
    # to get users who follow username
    followers = []
    users = User.objects.exclude(username=username)
    for user in users:
        friend, created = Friend.objects.get_or_create(current_user=user)
        following_user = friend.friend_list.all()
        if current_user in following_user:
            followers.append(user)

    # to get username following
    friend, created = Friend.objects.get_or_create(current_user=current_user)
    following = friend.friend_list.all()
    if User.objects.filter(username=username).exists():
        user = User.objects.get(username=username)
        return render(request, 'registration/user_profile.html', {'user': user, 'following': following,
                                                                  'followers': followers, 'following_request_user': following_request_user})
    else:
        return render(request, 'registration/user_not_found.html', {'username': username})


def edit_profile(request):
    if request.method == "POST":
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('user_profile', username=request.user.username)
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'registration/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })
