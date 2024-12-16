from django.core.management.base import BaseCommand

from faker import Faker
from django.contrib.auth import get_user_model
import random

User = get_user_model()

from games.models import Game,Developer,Genre,CountryDevelop,Platform



class Command(BaseCommand):
    def handle(self, *args, **options):

        users = User.objects.all()
        random_user = random.choice(list(users)) 

        fake = Faker(['ru_RU'])
        genres = ["Песочница", "Шутер", "Приключение", "Головоломка","Симулятор жизни", "RPG","MMORPG","Выживание","Ужастик","Стратегия"]
        platforms = ["ПК", "PlayStation", "Xbox", "Nintendo Switch", "Мобильные","VR","macOS","Xbox 360","PlayStation Portable"]

        for _ in range(10):
            genre_name = random.choice(genres)
            platform_name = random.choice(platforms)

             # Проверяем и создаем жанр, если его еще нет
            genre, _ = Genre.objects.get_or_create(name=genre_name)
            platform, _ = Platform.objects.get_or_create(name=platform_name)
            game_name = ' '.join(fake.words(nb=random.randint(1, 3)))
            country, _ = CountryDevelop.objects.get_or_create(name=fake.country())

            Game.objects.create(
                name=game_name,
                developer_fk=Developer.objects.create(name=fake.company(),
                                                      country_fk=country),
                genre_fk=genre,
                platform_fk=platform,
                user=random_user
            )
            