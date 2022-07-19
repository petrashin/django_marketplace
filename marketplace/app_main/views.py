from django.shortcuts import render
from django.views.generic import TemplateView


class BaseTemplateView(TemplateView):
    """ Вьюха для демонстрации базового шаблона """
    template_name = 'base.html'
    extra_context = {'title': "Megano"}


