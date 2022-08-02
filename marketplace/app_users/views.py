from django.contrib.auth.models import User
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView

from .forms import ReviewForm
from .models import Reviews, Categories


class BaseTemplateView(TemplateView):
    """ Вьюха для демонстрации базового шаблона """
    template_name = 'index.html'
    extra_context = {'title': "Megano"}

    def get_context_data(self, **kwargs):
        context = super(BaseTemplateView, self).get_context_data()
        context['categories'] = Categories.objects.filter(parent_category__isnull=True)
        return context


class AddReview(View):
    """ Отзыв """

    def get(self, request):
        return render(request, template_name='review.html',
                      context={'review_form': ReviewForm, 'reviews': Reviews.objects.all})

    def post(self, request):
        form = ReviewForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = User.objects.get(id=request.user.id)
            if request.POST.get("parent", None):
                form.parent_id = int(request.POST.get("parent"))
            form.save()

        return render(request, template_name='review.html',
                      context={'review_form': ReviewForm, 'reviews': Reviews.objects.all})
