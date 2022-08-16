from django.shortcuts import render
from app_users.models import Profile, Image
from django.views import View


def account_view(request):
    profile = Profile.objects.filter(user_id=request.user.id).get()
    avatar_object = Image.objects.filter(profile_id=profile)
    data = {
        "full_name": profile.fullname,
        "avatar": avatar_object[0].avatar
    }
    return render(request, "account.html", context=data)


class EditProfile(View):
    # TODO 1) отображение имеющейся аватарки, ФИО, телефона, почты
    # TODO 2) изменение всех данных
    def get(self, request):
        return render(request, "profile.html")
