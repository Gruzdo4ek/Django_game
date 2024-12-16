from rest_framework import serializers
from games.models import Game,Developer,Genre,Platform,CountryDevelop
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id','name']

class PlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = Platform
        fields = "__all__"

class CountryDevelopSerializer(serializers.ModelSerializer):
    class Meta:
        model = CountryDevelop
        fields = ['id','name','picture']

class DeveloperSerializer(serializers.ModelSerializer):
    country_fk=CountryDevelopSerializer(read_only=True)
    country_fk = serializers.PrimaryKeyRelatedField(queryset=CountryDevelop.objects.all())
    def create(self,validated_data):
        if 'request' in self.context:
            validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    class Meta:
        model = Developer
        fields = ['id', 'name', 'country_fk','user']

class GameSerializer(serializers.ModelSerializer):
    developer_fk=DeveloperSerializer(read_only=True)
    developer_fk = serializers.PrimaryKeyRelatedField(queryset=Developer.objects.all())
    genre_fk=GenreSerializer(read_only=True)
    genre_fk = serializers.PrimaryKeyRelatedField(queryset=Genre.objects.all())
    platform_fk=PlatformSerializer(read_only=True)
    platform_fk = serializers.PrimaryKeyRelatedField(queryset=Platform.objects.all())

    def create(self,validated_data):
        if 'request' in self.context:
            validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
    
    class Meta:
        model = Game
        fields = ['id','name','developer_fk','genre_fk','platform_fk','picture','user']