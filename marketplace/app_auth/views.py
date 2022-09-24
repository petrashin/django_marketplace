from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import PasswordResetForm
from app_auth.forms import SignUpForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import BadHeaderError, send_mail
from django.db.models.query_utils import Q
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from app_users.models import Profile, Role, Image


class Login(LoginView):
    """Класс авторизации пользователя"""
    template_name = 'login.html'


class Logout(LogoutView):
    """Класс, позволяющий разлогинить пользователя"""
    template_name = 'logout.html'


def register_view(request):
    """Вьюшка регистрации пользователя"""
    if request.method == 'POST':
        print(request.POST)
        if 'username' not in request.POST.keys():
            data = request.POST.copy()
            data['username'] = 'username' + str(User.objects.all().order_by('-id')[0].id)
            form = SignUpForm(data=data)
        else:
            form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            phone_number = form.cleaned_data.get('phone')
            fullname = form.cleaned_data.get('fullname')
            user = authenticate(username=username, password=raw_password)
            role = Role.objects.get_or_create(name='Пользователь')[0]
            profile = Profile.objects.create(user=user, role=role, phone_number=phone_number, fullname=fullname)
            Image.objects.create(profile=profile)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})


def password_reset_request(request):
    """Вьюшка восстановления пароля пользователя"""
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "password_reset_email.txt"
                    c = {
                        "email": user.email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'admin@example.com',
                                  [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect("password_reset_done")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="password_reset.html", context={"password_reset_form": password_reset_form})
