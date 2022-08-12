from django.db import models
from django.contrib.auth.models import User


class File(models.Model):
	file = models.FileField(upload_to='files/%Y-%m-%d')
	created_at = models.DateField(auto_now_add=True)
	user = models.ForeignKey(User, blank=True, on_delete=models.CASCADE)
