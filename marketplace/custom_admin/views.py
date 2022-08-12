from django.shortcuts import render
from django.views import View
from .forms import ImportGoodsForm


def admin_custom_settings(request):
	return render(request, template_name='admin/admin_custom_settings.html')
	
	
class ImportGoodsView(View):
	
	@staticmethod
	def get(request):
		file_form = ImportGoodsForm()
		return render(request, 'admin/admin_import_goods.html', context={'file_form': file_form})
	
	@staticmethod
	def post(request):
		user = request.user
		upload_file_form = ImportGoodsForm(request.POST, request.FILES)
		if upload_file_form.is_valid():
			list_goods = upload_file_form.cleaned_data.get('file').read().decode('utf-8').strip().split('\n')[1:]
			for product in list_goods:
				title, created_at = product.split(';')
				if not Product.objects.filter(title=title):
					new_product = Product.objects.create(title=title, created_at=created_at, user=user)
					new_product.save()
			return HttpResponseRedirect('/')
