from email.policy import default
import pathlib
from django.db import models
from urllib.parse import urlparse

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
    access_token = models.CharField(max_length=128, null=True)
    ignore_files = models.JSONField(default=list)
    folders = models.JSONField(default=list)
    link = models.URLField()

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.name
    
    @property
    def repo_name(self):
        return urlparse(self.repository).path.strip('/')


class AppUser(TimeStampedModel):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=512, default='')
    app = models.ForeignKey(App, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Functionality(TimeStampedModel):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=512)
    front_end_handler = models.CharField(max_length=128, null=True, blank=True)
    back_end_handler = models.CharField(max_length=128, null=True, blank=True)
    front_end_gist = models.CharField(max_length=128, null=True, blank=True)
    back_end_gist = models.CharField(max_length=128, null=True, blank=True)
    helpers = models.JSONField(default=list)
    procudure = models.JSONField(default=list)
    image = models.ImageField(upload_to=functionality_image_upload_location, null=True)
    app = models.ForeignKey(App, on_delete=models.CASCADE)
    users = models.ManyToManyField(AppUser, related_name='functionalities')

class File(TimeStampedModel):
    path = models.CharField(max_length=256)
    app = models.ForeignKey(App, on_delete=models.CASCADE)

    @property
    def dot_notation(self):
        path = pathlib.Path(self.path)
        return '.'.join(path.with_suffix('').parts)