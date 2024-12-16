"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from games import views
from games.api import GamesViewset,GenreViewset,PlatformViewset,CountryViewset,DeveloperViewset, UserProfileViewSet, UserViewSet
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register("games",GamesViewset,basename="games")
router.register("genre",GenreViewset,basename="genre")
router.register("platform",PlatformViewset,basename="platform")
router.register("developer",DeveloperViewset,basename="developer") 
router.register("country_developer",CountryViewset,basename="country_developer")
router.register("user", UserViewSet,basename="user")
router.register("user-profile", UserProfileViewSet, basename="user-profile")
router.register("export-excel",GamesViewset, basename="export-excel")
router.register("otp-login",UserViewSet, basename="otp-login")

urlpatterns = [
    path('',views.ShowGamesView.as_view()),
    path('',views.ShowGenreView.as_view()),
    path('',views.ShowPlatformView.as_view()),
    path('',views.ShowDeveloperView.as_view()),
    path('',views.ShowCountryView.as_view()),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
