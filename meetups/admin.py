from django.contrib import admin

from .models import MeetUp, Location, Participant

# Register your models here.


class MeetUpAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'date')
    list_display_links = ('title', 'location')
    list_filter = ('location', 'date')
    prepopulated_fields = {'slug': ['title']}
    search_fields = ('title', 'location')
    filter_horizontal = ['participants']


class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'address')
    list_display_links = ('name', 'address')
    list_filter = ('name', 'address')
    search_fields = ('name', 'address')


admin.site.register(MeetUp, MeetUpAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Participant)
