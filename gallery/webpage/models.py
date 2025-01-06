from django.db import models
from django.contrib.auth.models import User

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    count = models.IntegerField(default=0)

    class Meta:
        ordering = ['-count']

    def __str__(self):
        return self.name

class Project(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    description = models.TextField()
    video = models.URLField(max_length=200)
    thumbnail = models.URLField(max_length=200)
    tags = models.ManyToManyField(Tag, through='ProjectTag')

    def __str__(self):
        return self.title

class ProjectTag(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('project', 'tag')

    def __str__(self):
        return f'{self.project.title} - {self.tag.name}'
    

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
