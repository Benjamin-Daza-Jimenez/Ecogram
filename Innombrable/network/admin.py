from django.contrib import admin
from . import models
from .models import Post
from .models import Imagenes_del_sitio

admin.site.register(models.Imagenes_del_sitio)
admin.site.register(models.Comentarios)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('identifier',)} 
