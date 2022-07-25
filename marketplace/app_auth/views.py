from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.shortcuts import redirect


class Login(LoginView):
    template_name = 'login.html'


class Logout(LogoutView):
    template_name = 'logout.html'


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('../../')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})
