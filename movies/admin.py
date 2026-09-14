from django.contrib import admin
from .models import Movie, Review, ReviewReport


class MovieAdmin(admin.ModelAdmin):
    ordering = ['name']
    search_fields = ['name']
    list_display = ['id', 'name', 'price']


class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'movie', 'user', 'is_hidden', 'date']
    list_filter = ['is_hidden', 'date']
    search_fields = ['comment', 'user__username', 'movie__name']


class ReviewReportAdmin(admin.ModelAdmin):
    list_display = ['id', 'review', 'user', 'reason', 'date']
    search_fields = ['reason', 'user__username']


admin.site.register(Movie, MovieAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(ReviewReport, ReviewReportAdmin)
