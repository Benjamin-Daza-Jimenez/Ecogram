import random
import string

from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin, User)
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.conf import settings
from network.models import Post
from .forms import UserChangeForm

def rand_slug():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6))
    

class CustomAccountManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password, **other_fields):
       
        if not email:
            raise ValueError(_('You must provide an email adress'))
        
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name,
                          last_name=last_name, **other_fields)
        user.set_password(password)
        user.save()
        return user
   
    def create_superuser(self, email, first_name, last_name, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')
        
        return self.create_user(email, first_name, last_name, password, **other_fields)


class UserProfile(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique= True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    profile_pic= models.ImageField(
        upload_to='users/', default='users/default.png')
    bio = models.TextField(_(
        'Bio'), max_length=500, blank=True)
    followers = models.ManyToManyField(
        'self',
        blank=True,
        related_name='followers')
    slug = models.SlugField(max_length=255, unique=True)

    register_date = models.DateTimeField(default=timezone.now)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def get_absolute_url(self):
        return reverse('users:user_detail', args=[self.slug])

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(rand_slug() + "-" + self.email)
        super(UserProfile, self).save(*args, **kwargs)\

    def count_following(self):
        user_following = UserProfile.objects.filter(followers=self)
        return user_following.count()
    
    def count_posts(self):
        return Post.objects.filter(author=self).count()

    def is_follower(self, other_user):
        if UserProfile.objects.filter(followers=other_user):
            return True
        return False

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(rand_slug() + '-' + self.email)
        super(UserProfile, self).save(*args, **kwargs)

class EditProfile(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ('profile_pic',)

