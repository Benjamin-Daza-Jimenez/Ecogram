from django.db import models
from django.db.models.signals import pre_save
from django.conf import settings
User = settings.AUTH_USER_MODEL
from django.utils import timezone
from django.utils.text import slugify
import uuid


class Post(models.Model):
    identifier = models.UUIDField(primary_key=True, default=uuid.uuid4)
    slug = models.SlugField(max_length=250, null=False, blank=False, unique=True)
    title = models.CharField(max_length=100, default='Título')
    description = models.TextField()
    image = models.ImageField(upload_to='images/', default='images/default_banner.png')
    published = models.DateTimeField(default=timezone.now)
    likes = models.ManyToManyField(User, blank=True, related_name='likes')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
        related_name='network_post'
    )

    class Meta:
        ordering = ('-published',)
    
    def __str__(self):
        return self.title
    def cantidad_likes(self):
        return self.likes.count()

def generate_slug(string):
    id = str(uuid.uuid4())
    return slugify('{}-{}'.format(string, id[:8]))
def set_slug(sender, instance, *args, **kwargs):
    if instance.slug:
        return
    slug = generate_slug(instance.title)

    while(Post.objects.filter(slug=slug).exists()):
        slug = generate_slug(instance.title)
    instance.slug = slug

pre_save.connect(set_slug, sender=Post)

class Imagenes_del_sitio(models.Model):
    image = models.ImageField(upload_to='images/')
    title = models.CharField(max_length=100, default='Título')
    
    def __str__(self):
        return self.title

class Comentarios(models.Model):
    comment = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='social_comment_author')
    post = models.ForeignKey('Post', on_delete=models.CASCADE, default="")
    created_on = models.DateTimeField(default=timezone.now)
    likes = models.ManyToManyField(User, blank=True, related_name='comment_likes')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='+')
    
    @property
    def children(self):
        return Comentarios.objects.filter(parent=self).order_by('-created_on').all()

    @property
    def is_parent(self):
        if self.parent is None:
            return True
        return False