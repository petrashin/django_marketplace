from django import forms

#
# class ImportGoodsForm(forms.Form):
# 	file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))


class ImportGoodsForm(forms.Form):
	file = forms.FileField(required=False)