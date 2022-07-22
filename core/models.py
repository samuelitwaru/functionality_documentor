from email.policy import default
from django.db import models


def functionality_image_upload_location(instance, filename):
    _, extension = filename.split('.')
    return f'teachers/pictures/{instance.id}.{extension}'

# Create your models here.
class TimeStampedModel(models.Model):
	created_at = models.DateTimeField(auto_now_add=True, null=True)
	updated_at = models.DateTimeField(auto_now=True, null=True)

	class Meta:
		abstract = True


class App(TimeStampedModel):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=512)
    repository = models.URLField()
    link = models.URLField()

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.name


class AppUser(TimeStampedModel):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=512, default='')
    app = models.ForeignKey(App, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Functionality(TimeStampedModel):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=512)
    handler = models.CharField(max_length=128)
    helpers = models.JSONField(default=list)
    procudure = models.JSONField(default=list)
    image = models.ImageField(upload_to=functionality_image_upload_location, null=True)
    app = models.ForeignKey(App, on_delete=models.CASCADE)
    users = models.ManyToManyField(AppUser, related_name='functionalities')