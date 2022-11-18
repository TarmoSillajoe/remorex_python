from django.db import models
from django.template.defaultfilters import slugify


class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(blank=True)
    content = models.TextField()
    overview = models.TextField(null=True)
    thumbnail = models.ImageField(upload_to="images/", null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title[:20])
        super(Post, self).save(*args, **kwargs)
