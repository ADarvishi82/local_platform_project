# posts/admin.py
from django.contrib import admin
from .models import Post,Like,Comment, Event

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'content_summary', 'created_at', 'updated_at')
    list_filter = ('author', 'created_at')
    search_fields = ('author__username', 'content')
    readonly_fields = ('created_at', 'updated_at')

    def content_summary(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_summary.short_description = "خلاصه محتوا"
    

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'post__content') 
    
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('author__username', 'post__content')
    readonly_fields = ('created_at', 'updated_at')

    def content_summary(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_summary.short_description = "خلاصه محتوا"
    
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'neighborhood',
        'creator',
        'start_time',
        'end_time',
        'location_name',
        'is_approved',
        'created_at',
    )
    list_filter = (
        'is_approved',
        'neighborhood',
        'start_time',
        'creator',
    )
    search_fields = (
        'title',
        'description',
        'location_name',
        'creator__username',
        'neighborhood__name',
    )
    date_hierarchy = 'start_time'
    ordering = ['-start_time']
    readonly_fields = ('created_at', 'updated_at')

    