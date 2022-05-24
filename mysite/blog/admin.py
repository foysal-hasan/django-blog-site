from django.contrib import admin

from blog.models import Post, Comment

# Register your models here.

# admin.site.register(Post)
# admin.site.register(Comment)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id','author', 'title', 'text',
                    'created_date', 'published_date']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id','post', 'author', 'text', 'created_date']
