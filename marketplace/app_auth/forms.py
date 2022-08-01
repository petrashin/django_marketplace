from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email",)

    def clean(self):
       email = self.cleaned_data.get('email')
       username = self.cleaned_data.get('username')
       if User.objects.filter(email=email).exists():
            raise ValidationError("Email exists")
       elif User.objects.filter(username=username).exists():
            raise ValidationError("Username exists")
       return self.cleaned_data