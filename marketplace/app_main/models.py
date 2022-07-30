from django.db import models


class Categories(models.Model):
    name = models.CharField(max_length=25)
    parent_category = models.ForeignKey('self', null=True, blank=True, on_delete=models.DO_NOTHING, related_name="sub")
    category_icon = models.FileField(upload_to='static/assets/img/icons/departments/')

    def __str__(self):
        return self.name
