from django.views.generic import TemplateView

# BaseTemplateView перенес в app_shops.views


class ProfileTemplateView(TemplateView):
    """ Профиль пользователя """
    template_name = 'profile.html'

