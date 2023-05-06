from cgitb import lookup
from email.mime import image
from django.conf import settings
from django.db import models
from django.db.models import Q
from django.utils import timezone

User = settings.AUTH_USER_MODEL

class BlogPostQuerySet(models.QuerySet):
    def published(self):
        now = timezone.now()
        return self.filter(publish_date__lte=now) # same as BlogPost.objects.filter()
    
    def search(self, query):
        lookup = (
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(slug__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query) |
            Q(user__email__icontains=query) |
            Q(user__username__icontains=query)
        )

        return self.filter(lookup)


class BlogPostManager(models.Manager):
    # Call using objects.all().published()
    def get_queryset(self):
        return BlogPostQuerySet(self.model, using=self.db)

    # Call using objects.published()
    def published(self):
        now = timezone.now()
        return self.get_queryset().filter(publish_date__lte=now) # same as BlogPost.objects.filter()

    def search(self, query=None):
        if query is None:
            return self.get_queryset().none()
        # return self.get_queryset().search(query)
        return self.get_queryset().published().search(query)

class BlogPost(models.Model):
    user            = models.ForeignKey(User, default=1, null=True, on_delete=models.SET_NULL) # default super user
    image           = models.ImageField(upload_to='image/', blank=True, null=True)
    title           = models.CharField(max_length=120)
    slug            = models.SlugField(unique=True)
    content         = models.TextField(null=True, blank=True)
    publish_date    = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    timestamp       = models.DateTimeField(auto_now_add=True)
    updated         = models.DateTimeField(auto_now=True)

    objects = BlogPostManager()

    class Meta:
        ordering = ['-publish_date', '-updated', '-timestamp'] # '-field' = desc

    def get_absolute_url(self):
        return f"/blog/{self.slug}"

    def get_edit_url(self):
        # return f"/blog/{self.slug}/edit"
        return f"{self.get_absolute_url()}/edit"

    def get_delete_url(self):
        return f"{self.get_absolute_url()}/delete"
