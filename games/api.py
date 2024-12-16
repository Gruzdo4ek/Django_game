from rest_framework.viewsets import GenericViewSet
from games.models import Game,Genre,Platform,CountryDevelop,Developer
from rest_framework import mixins,viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.models import User
from rest_framework.exceptions import PermissionDenied
from games.serializers import GameSerializer,GenreSerializer,PlatformSerializer,DeveloperSerializer,CountryDevelopSerializer,UserSerializer
from django.db.models import Avg, Count,Max,Min
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated, BasePermission
from django.contrib.auth import authenticate, login
from django.core.cache import cache  
from django.http import HttpResponse
import pandas as pd
import pyotp

class OTPRequired(BasePermission):
    def has_permission(self, request, view):
        otp_good = cache.get('otp_good', False)
        if otp_good:
            return True
        return False


class GamesViewset(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet
):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

    # Применяем разрешение OTPRequired для действий обновления
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_authenticated:
            if not self.request.user.is_superuser:
                qs = qs.filter(user=self.request.user)
        else:
            qs = Game.objects.none()
        return qs

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return GameSerializer
        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            raise PermissionDenied("Вы должны быть авторизованы для выполнения этого действия.")
        
        
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            raise PermissionDenied("Вы должны быть авторизованы для выполнения этого действия.")
        
        
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            raise PermissionDenied("Вы должны быть авторизованы для выполнения этого действия.")
        
        
        return super().destroy(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            raise PermissionDenied("Вы должны быть авторизованы для выполнения этого действия.")
        return super().retrieve(request, *args, **kwargs)
    
    class StatsSerializer(serializers.Serializer):
        count=serializers.IntegerField()

    @action(detail=False,methods=['GET'],url_path='stats')
    def get_stats(self,request,*args,**kwargs):
        stats=Game.objects.aggregate(
            count=Count("*"),
        )
        serializer=self.StatsSerializer(instance=stats)
        return Response(serializer.data)
    
    @action(detail=False, methods=["GET"], url_path="export-excel")
    def export_excel(self, request):
        queryset = self.get_queryset()
        df = pd.DataFrame(queryset.values())
        response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=games.xlsx'
        df.to_excel(response, index=False)
        return response


                

class GenreViewset(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet
):
    
    queryset=Genre.objects.all()
    serializer_class=GenreSerializer

    class StatsSerializer(serializers.Serializer):
        count=serializers.IntegerField()

    @action(detail=False,methods=['GET'],url_path='stats')
    def get_stats(self,request,*args,**kwargs):
        stats=Genre.objects.aggregate(
            count=Count("*"),
        )
        serializer=self.StatsSerializer(instance=stats)
        return Response(serializer.data)

class PlatformViewset(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet
):
    
    queryset=Platform.objects.all()
    serializer_class=PlatformSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_authenticated:
            if not self.request.user.is_superuser:
                qs = qs.filter(user=self.request.user)
        else:
            qs = Platform.objects.none()
        return qs

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return PlatformSerializer
        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            raise PermissionDenied("Вы должны быть авторизованы для выполнения этого действия.")
        return super().create(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            raise PermissionDenied("Вы должны быть авторизованы для выполнения этого действия.")
        return super().retrieve(request, *args, **kwargs)

    class StatsSerializer(serializers.Serializer):
        count=serializers.IntegerField()

    @action(detail=False,methods=['GET'],url_path='stats')
    def get_stats(self,request,*args,**kwargs):
        stats=Platform.objects.aggregate(
            count=Count("*"),
        )
        serializer=self.StatsSerializer(instance=stats)
        return Response(serializer.data)

class DeveloperViewset(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet
):
    
    queryset=Developer.objects.all()
    serializer_class=DeveloperSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_authenticated:
            if not self.request.user.is_superuser:
                qs = qs.filter(user=self.request.user)
        else:
            qs = Developer.objects.none()
        return qs

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return DeveloperSerializer
        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            raise PermissionDenied("Вы должны быть авторизованы для выполнения этого действия.")
        return super().create(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            raise PermissionDenied("Вы должны быть авторизованы для выполнения этого действия.")
        return super().retrieve(request, *args, **kwargs)

    class StatsSerializer(serializers.Serializer):
        count=serializers.IntegerField()

    @action(detail=False,methods=['GET'],url_path='stats')
    def get_stats(self,request,*args,**kwargs):
        stats=Developer.objects.aggregate(
            count=Count("*"),
        )
        serializer=self.StatsSerializer(instance=stats)
        return Response(serializer.data)

class CountryViewset(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet
):
    
    queryset=CountryDevelop.objects.all()
    serializer_class=CountryDevelopSerializer

    class StatsSerializer(serializers.Serializer):
        count=serializers.IntegerField()

    @action(detail=False,methods=['GET'],url_path='stats')
    def get_stats(self,request,*args,**kwargs):
        stats=CountryDevelop.objects.aggregate(
            count=Count("*"),
        )
        serializer=self.StatsSerializer(instance=stats)
        return Response(serializer.data)

class UserViewSet( mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    


class UserProfileViewSet(GenericViewSet):
    permission_classes = [IsAuthenticated]

    class OTPSerializer(serializers.Serializer):
        key = serializers.CharField()

    class OTPRequired(BasePermission):
        def has_permission(self, request, view):
            return bool(request.user and cache.get('otp_good', False))
        
    @action(detail=False, methods=['get'], url_path='info')
    def get_info(self, request, *args, **kwargs):
        user = request.user
        data = {
           "is_authenticated": self.request.user.is_authenticated
        }
        if self.request.user.is_authenticated:
           data.update({
               "is_superuser":self.request.user.is_superuser,
               "name": self.request.user.username
            })
        return Response(data)  
     
    @action(detail=False, url_path="check-login", methods=['GET'], permission_classes=[])
    def get_check_login(self, request, *args, **kwargs):
        return Response({
            'is_authenticated': self.request.user.is_authenticated
        })
    
    @action(detail=False, url_path="login", methods=['GET'], permission_classes=[])
    def use_login(self, request, *args, **kwargs):
        user= authenticate(username='username', password='pass')
        if user:
            login(request, user)
        return Response({
            'is_authenticated': bool(user)
        })

    @action(detail=False, url_path='otp-login', methods=['POST'])
    def otp_login(self, *args, **kwargs):
        # Этот код всегда будет считать OTP верным
        cache.set('otp_good', True, 300)  # Сохраняем успешный статус OTP в кэш (на 5 минут)

        # Устанавливаем переменную success как True
        success = True

        return Response({
            'success': success
        })
    
    @action(detail=False, url_path='otp-status')
    def get_otp_status(self, *args, **kwargs):
        otp_good = cache.get('otp_good', False)  # Получаем статус OTP из кэша
        return Response({
            'otp_good': otp_good
        })
    
    @action(detail=False, url_path='otp-required', permission_classes=[OTPRequired])
    def page_with_otp_required(self, *args, **kwargs):
        return Response({
            'success': True
        })
