from django.shortcuts import render
from app_users.models import Profile, Image


def account_view(request):
    profile = Profile.objects.filter(user_id=request.user.id).get()
    avatar_object = Image.objects.filter(profile_id=profile)
    data = {
        "full_name": f"{request.user.first_name} {request.user.last_name}",
        "avatar": avatar_object[0].avatar
    }
    return render(request, "account.html", context=data)
