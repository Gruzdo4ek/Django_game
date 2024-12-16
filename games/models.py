from django.db import models


class CountryDevelop(models.Model):
    name=models.TextField("Страна разработки")
    picture = models.ImageField("Изображение", null=True, upload_to="country_developer")

    class Meta:
        verbose_name="Страна разработки"
        verbose_name_plural="Страны разработки"
    def __str__(self) -> str:
        return self.name
    
class Platform(models.Model):
    name=models.TextField("Платформа")

    class Meta:
        verbose_name="Платформа"
        verbose_name_plural="Платформы"
    def __str__(self) -> str:
        return self.name

class Genre(models.Model):
    name=models.TextField("Жанр")

    class Meta:
        verbose_name="Жанр"
        verbose_name_plural="Жанры"
    def __str__(self) -> str:
        return self.name
    
class Developer(models.Model):
    name=models.TextField("Название")
    country_fk=models.ForeignKey("CountryDevelop",on_delete=models.CASCADE,null=True)
    user = models.ForeignKey("auth.User",verbose_name="Пользователь",on_delete=models.CASCADE,null=True)

    class Meta:
        verbose_name="Разработчик"
        verbose_name_plural="Разработчики"
    def __str__(self) -> str:
        return self.name


class Game(models.Model):
    name=models.TextField("Название")
    developer_fk=models.ForeignKey("Developer",on_delete=models.CASCADE,null=True)
    genre_fk=models.ForeignKey("Genre",on_delete=models.CASCADE,null=True)
    platform_fk=models.ForeignKey("Platform",on_delete=models.CASCADE,null=True)
    picture = models.ImageField("Изображение", null=True, upload_to="games")
    user = models.ForeignKey("auth.User",verbose_name="Пользователь",on_delete=models.CASCADE,null=True)
    
    class Meta:
        verbose_name="Игра"
        verbose_name_plural="Игры"
