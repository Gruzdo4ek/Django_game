from django.shortcuts import render
from django.http import HttpResponse
from games.models import Game,Genre,Platform,Developer,CountryDevelop
from django.views import View
from django.views.generic import TemplateView

class ShowGamesView(TemplateView):
    template_name="games/show_games.html"
    def get_context_data(self,**kwargs:any)->dict[str,any]:
        context=super().get_context_data(**kwargs)
        context['games']=Game.objects.all()
        
        return context

class ShowGenreView(TemplateView):
    template_name="genre/show_games.html"
    def get_context_data(self,**kwargs:any)->dict[str,any]:
        context=super().get_context_data(**kwargs)
        context['genre']=Genre.objects.all()

        return context
    
class ShowPlatformView(TemplateView):
    template_name="platform/show_games.html"
    def get_context_data(self,**kwargs:any)->dict[str,any]:
        context=super().get_context_data(**kwargs)
        context['platform']=Platform.objects.all()

        return context
    
class ShowDeveloperView(TemplateView):
    template_name="developer/show_games.html"
    def get_context_data(self,**kwargs:any)->dict[str,any]:
        context=super().get_context_data(**kwargs)
        context['developer']=Developer.objects.all()

        return context
    
class ShowCountryView(TemplateView):
    template_name="country_developer/show_games.html"
    def get_context_data(self,**kwargs:any)->dict[str,any]:
        context=super().get_context_data(**kwargs)
        context['country']=CountryDevelop.objects.all()

        return context