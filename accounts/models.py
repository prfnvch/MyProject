from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.urls import reverse
from .managers import UserManager
from django.utils.translation import gettext_lazy as _


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=60, unique=True)
    email = models.EmailField(unique=True)

    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    avatar = models.ImageField(null=True, blank=True, upload_to="avatars/")
    bio = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    date_of_birth = models.DateTimeField(blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    instagram = models.CharField(max_length=100, blank=True)
    telegram = models.CharField(max_length=100, blank=True)

    bookmarks = models.ManyToManyField("main.Manga", blank=True, related_name='related_manga')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return self.username
    
    def get_user_url(self):
        return reverse("user", args=[self.id])

    def follows_count(self):
        return len(self.bookmarks.all())
    
    def get_follow_url(self):
        return reverse("manga-follow", args=[self.id])



