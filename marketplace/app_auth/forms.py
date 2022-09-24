from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from app_users.models import Profile


class SignUpForm(UserCreationForm):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits "
                                         "allowed.")
    phone = forms.CharField(validators=[phone_regex], max_length=17)
    fullname = forms.CharField(max_length=256, required=True)

    class Meta:
        model = User
        fields = ("username", "email", "phone", "fullname")

    def clean(self):
       
       email = self.cleaned_data.get('email')
       username = self.cleaned_data.get('username')
       phone = self.cleaned_data.get('phone')
       if User.objects.filter(email=email).exists():
            raise ValidationError("Email exists")
       elif User.objects.filter(username=username).exists():
            raise ValidationError("Username exists")
       elif Profile.objects.filter(phone_number=phone).exists():
            raise ValidationError("Phone number exists")
       return self.cleaned_data