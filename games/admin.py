from django.contrib import admin
from games.models import Genre, Platform, Developer,Game,CountryDevelop
# Register your models here.

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display=['id','name','developer_fk','genre_fk','platform_fk','picture','user']

@admin.register(Developer)
class DeveloperAdmin(admin.ModelAdmin):
    list_display=['id','name','country_fk','user']

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display=['id','name']

@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
    list_display=['id','name']

@admin.register(CountryDevelop)
class CountryDevelopAdmin(admin.ModelAdmin):
    list_display=['id','name','picture']