import re
from django.shortcuts import render
from app_users.models import Profile, Image
from django.views import View
from django.contrib.auth.models import User


def account_view(request):
    profile = Profile.objects.filter(user_id=request.user.id).get()
    avatar_object = Image.objects.filter(profile_id=profile)
    data = {
        "full_name": profile.fullname,
        "avatar": avatar_object[0].avatar
    }
    return render(request, "account.html", context=data)


def validate_fullname(string):
    return len(re.findall(r'\w+', string)) == 3


def validate_phone(string):
    if re.match(r'(\+7|8).*?(\d{3}).*?(\d{3}).*?(\d{2}).*?(\d{2})', string) and len(string) == 12:
        return True
    return False


def validate_email(string):
    if re.match(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+', string):
        return True
    return False


def validate_passwords(s, s_rep):
    """
    Пароль должен состоять по крайней мере из восьми символов, содержат символы в верхнем и нижнем регистрах и
    включать по крайней мере одну цифру
    """
    if re.match(r'^(?=.*[0-9].*)(?=.*[a-z].*)(?=.*[A-Z].*)[0-9a-zA-Z]{8,}$', s) and s == s_rep:
        return True
    return False


class EditProfile(View):
    def get(self, request):
        profile = Profile.objects.filter(user_id=request.user.id).get()
        data = {
            "avatar_correct": True,
            "full_name": profile.fullname,
            "name_correct": True,
            "phone_number": profile.phone_number,
            "phone_correct": True,
            "email": request.user.email,
            "email_correct": True,
            "passwords_correct": True,
        }
        return render(request, "profile.html", context=data)

    def post(self, request):
        # TODO: возможно, отслеживать только измененные поля
        #  чтобы при изменении ФИО и оставлении полей паролей пустыми не появлялись ошибки

        user = User.objects.get(id=request.user.id)
        profile = Profile.objects.filter(user_id=request.user.id).get()
        data = {}

        # TODO: валидация и смена аватарки (не более 2 Мбайт)
        data["avatar_correct"] = True

        new_fullname = request.POST.get("name")

        if validate_fullname(new_fullname):
            profile.fullname = new_fullname
            profile.save()
            data["full_name"] = new_fullname
            data["name_correct"] = True
        else:
            data["full_name"] = profile.fullname
            data["name_correct"] = False

        new_phone = request.POST.get("phone")

        if validate_phone(new_phone) and not Profile.objects.filter(phone_number=new_phone).exists() or new_phone == profile.phone_number:
            # TODO: для неправильного телефона и повторяющегося телефона должны выводиться разные ошибки
            profile.phone_number = new_phone
            profile.save()
            data["phone_number"] = new_phone
            data["phone_correct"] = True
        else:
            data["phone_number"] = profile.phone_number
            data["phone_correct"] = False

        # TODO: валидация и смена email (email также не должен повторяться).
        # TODO: Для неправильного email и повторяющегося email должны выводиться разные ошибки
        data["email"] = request.user.email
        data["email_correct"] = True

        new_password = request.POST.get("password")
        new_password_reply = request.POST.get("passwordReply")

        if validate_passwords(new_password, new_password_reply) and new_password:
            # TODO: для несовпадающих паролей и для слишком простых паролей должны выводиться разные ошибки
            user.set_password(new_password)
            user.save()
            data["passwords_correct"] = True
        else:
            data["passwords_correct"] = False

        if data["avatar_correct"] and data["name_correct"] and data["phone_correct"] and data["email_correct"] and data["passwords_correct"]:
            data["changed_successfully"] = True
        else:
            data["changed_successfully"] = False

        return render(request, "profile.html", context=data)
