from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateFrom, ForgetPasswordForm, ResetPasswordForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from users.models import UserOTP
from users.utils import generateOTP
from django.urls import reverse
from django.core.mail import send_mail
from MyBlog import settings


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            first_name = form.cleaned_data.get('first_name')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            User.objects.create_user(username, email, password, first_name=first_name)
            messages.add_message(request, messages.SUCCESS, "User created successfully")
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST,
                                instance=request.user)
        p_form = ProfileUpdateFrom(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your Profile is Updated')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateFrom(instance=request.user.profile)
    context = {
        'u_form': u_form,
        'p_from': p_form
    }
    return render(request, 'users/profile.html', context)


class ForgotPasswordView(TemplateView):
    template_name = 'users/forget_password.html'
    form_class = ForgetPasswordForm

    def get_context_data(self, **kwargs):
        context = {}
        context['form'] = self.form_class
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            print(email)
            user = User.objects.filter(email=email).first()
            if user is not None:
                otp = UserOTP()
                otp.user = user
                otp.otp = generateOTP(10)
                otp.save()

                otp_reset_url = reverse('reset_password')
                print("Forget password",
                          "sending email with password reset link {}{}?username={}&otp={}"
                      .format(settings.SERVER_URL, otp_reset_url, user.username, otp.otp))

                send_mail(
                        "Forget password",
                        "sending email with password reset link {}{}?username={}&otp={}"
                          .format(settings.SERVER_URL, otp_reset_url, user.username, otp.otp), 'RockyBlog@gmail.com', [email])

                # context = self.get_context_data(request=request)
                messages.add_message(self.request, messages.ERROR, "Please Check Your Email For OTP")
                return redirect('forget_password')
            context = self.get_context_data(request=request)
            messages.add_message(self.request, messages.ERROR, "Invalid Email Address")
            return render(request, self.template_name, context=context)


class ResetPasswordView(TemplateView):
    template_name = 'users/password_reset.html'
    form_class = ResetPasswordForm

    def get_context_data(self, **kwargs):
        context = {}
        context['form'] = self.form_class
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            repeatpassword = form.cleaned_data['repeatpassword']
            otp = form.cleaned_data['otp']
            user = User.objects.filter(username=username).first()
            if user is not None:
                if password != repeatpassword:
                    context = self.get_context_data(request=request)
                    messages.add_message(self.request, messages.ERROR, "Password Mismatch")
                    return render(request, self.template_name, context=context)
                otpObj = UserOTP.objects.filter(user=user, otp=otp).first()
                if otpObj is not None:
                    if otpObj.isvalid == True:
                        user.set_password(password)
                        user.save()
                        otpObj.isvalid = False
                        otpObj.save()
                        messages.add_message(self.request, messages.ERROR, "Password Reset Successfully")
                        return redirect('login')
                    else:
                        context = self.get_context_data(request=request)
                        messages.add_message(self.request, messages.ERROR, "OTP link expired")
                        return render(request, self.template_name, context=context)
                context = self.get_context_data(request=request)
                messages.add_message(self.request, messages.ERROR, "Invalid OTP")
                return redirect('login')
            context = self.get_context_data(request=request)
            return render(request, self.template_name, context=context)

















