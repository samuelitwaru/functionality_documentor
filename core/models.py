import pathlib
from re import A
from tokenize import blank_re
from urllib.parse import urlparse

from django.db import models
from django_quill.fields import QuillField

from core.utils import END_CHOICES, dot_notation
from django.contrib.auth.models import User


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

    fe_repo = models.URLField(null=True, blank=True)
    fe_token = models.CharField(max_length=128, null=True, blank=True)
    fe_ignore_files = models.JSONField(default=list, blank=True)
    fe_folders = models.JSONField(default=list, blank=True)
    fe_link = models.URLField(null=True, blank=True)

    be_repo = models.URLField(null=True, blank=True)
    be_token = models.CharField(max_length=128, null=True, blank=True)
    be_ignore_files = models.JSONField(default=list, blank=True)
    be_folders = models.JSONField(default=list, blank=True)
    be_link = models.URLField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    collaborators = models.ManyToManyField(User, related_name='apps')

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.name

    @property
    def fe_repo_name(self):
        return urlparse(self.fe_repo).path.strip('/')

    @property
    def be_repo_name(self):
        return urlparse(self.be_repo).path.strip('/')

    @property
    def fe_file_set(self):
        return self.file_set.filter(end='FRONT')

    @property
    def be_file_set(self):
        return self.file_set.filter(end='BACK')


class AppUser(TimeStampedModel):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=512, default='')
    app = models.ForeignKey(App, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Functionality(TimeStampedModel):
    name = models.CharField(max_length=64)
    # description = models.CharField(max_length=512)
    description = QuillField()
    front_end_file = models.CharField(max_length=128, null=True, blank=True)
    back_end_file = models.CharField(max_length=128, null=True, blank=True)
    front_end_handler = models.CharField(max_length=128, null=True, blank=True)
    back_end_handler = models.CharField(max_length=128, null=True, blank=True)
    front_end_gist = models.CharField(max_length=128, null=True, blank=True)
    back_end_gist = models.CharField(max_length=128, null=True, blank=True)
    helpers = models.JSONField(default=list, null=True, blank=True)
    procudure = models.JSONField(default=list, null=True, blank=True)
    image = models.ImageField(
        upload_to=functionality_image_upload_location, null=True, blank=True)
    app = models.ForeignKey(App, on_delete=models.CASCADE)
    users = models.ManyToManyField(AppUser, related_name='functionalities')
    user_manual = QuillField(null=True, blank=True)
    user_video = models.URLField(max_length=1024, null=True, blank=True)
    dev_manual = models.CharField(max_length=1024, null=True, blank=True)
    dev_video = models.URLField(null=True, blank=True)

    def __str__(self):
        return f'{self.app} {self.name}'

    def fe_handler(self):
        file_path = self.front_end_file
        handler = self.front_end_handler
        return f'{file_path} => {handler}'

    def be_handler(self):
        file_path = self.back_end_file
        handler = self.back_end_handler
        return f'{file_path} => {handler}'


class File(TimeStampedModel):
    path = models.CharField(max_length=256)
    end = models.CharField(max_length=8, choices=END_CHOICES, default='FRONT')
    app = models.ForeignKey(App, on_delete=models.CASCADE)

    def __str__(self):
        return self.path

    @property
    def dot_notation(self):
        path = pathlib.Path(self.path)
        return '.'.join(path.with_suffix('').parts)
    
class FunctionalityCategory(TimeStampedModel):
     name = models.CharField(max_length=32)
     description = models.CharField(max_length=128)
     Functionalities = models.ManyToManyField(Functionality, related_name='categories')
     
     def __str__(self):
         return self.name
