from django.contrib.auth.models import User
from django.shortcuts import render
from django.views import View

from .forms import ReviewForm
from .models import Reviews


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
