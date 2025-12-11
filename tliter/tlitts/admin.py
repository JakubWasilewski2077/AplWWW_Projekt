from django.contrib import admin
from .models import Tlitt, Comment, Hashtag ,Like, Follow

# Register your models here.

class TlittAdmin(admin.ModelAdmin):
    readonly_fields = ['created_at']
    list_display = ['id', 'content_skr', 'creator', 'created_at']
    search_fields = ['author__username', 'contents']
    list_filter = ['created_at']
    ordering = ['-created_at']

    def content_skr(self, obj):
        contents_skr = obj.contents.split()
        if len(contents_skr) <= 10:
            return obj.contents
        return " ".join(contents_skr[:10]) + "..."

class CommentAdmin(admin.ModelAdmin):
    readonly_fields = ['created_at']
    list_display = ['id', 'content_skr', 'creator', 'tlitt' ,'created_at']
    search_fields = ['author__username', 'contents']
    list_filter = ['created_at']
    ordering = ['-created_at']

    def content_skr(self, obj):
        contents_skr = obj.contents.split()
        if len(contents_skr) <= 10:
            return obj.contents
        return " ".join(contents_skr[:10]) + "..."

class HashtagAdmin(admin.ModelAdmin):
    list_display = ['id', 'contents', 'tlitt_number']
    search_fields = ['contents']
    ordering = ['contents']

    def tlitt_number(self, obj):
        return obj.tlitts.count()

    tlitt_number.short_description = 'liczba tlitt'

class LikeAdmin(admin.ModelAdmin):
    list_display = ['id','user','tlitt']
    search_fields = ['user__username']

class FollowAdmin(admin.ModelAdmin):
    list_display = ['id','follower','following']
    search_fields = ['follower__username','following__username']
    ordering = ['following__username']


admin.site.register(Tlitt,TlittAdmin)
admin.site.register(Comment,CommentAdmin)
admin.site.register(Hashtag,HashtagAdmin)
admin.site.register(Like,LikeAdmin)
admin.site.register(Follow,FollowAdmin)