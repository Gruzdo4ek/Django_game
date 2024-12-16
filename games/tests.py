from django.test import TestCase
from games.models import Game,Developer,Platform,CountryDevelop,Genre
from rest_framework.test import APIClient
from model_bakery import baker

# Create your tests here.
class GamesViewsetTestCase(TestCase):
    def setUp(self):
        self.client=APIClient()

    def test_get_list(self):
        gnr = baker.make("Genre")
        plt = baker.make("Platform")
        dvl = baker.make("Developer")

        game = baker.make("Game",genre_fk=gnr,platform_fk=plt,developer_fk=dvl)

        r=self.client.get('/api/games/')
        data=r.json()
        print(data)

        assert game.name == data[0]['name']
        assert game.id == data[0]['id']
        assert game.genre_fk.id == data[0]['genre_fk']
        assert game.platform_fk.id == data[0]['platform_fk']
        assert game.developer_fk.id == data[0]['developer_fk']
        assert len(data)==1

    def test_create_game(self):
        gnr = baker.make("Genre")
        plt = baker.make("Platform")
        dvl = baker.make("Developer")

        r = self.client.post("/api/games/", {
            "name": "Игра",
            "genre_fk": gnr.id,
            "platform_fk": plt.id,
            "developer_fk": dvl.id
        })

        new_game_id = r.json()['id']

        games = Game.objects.all()
        assert len(games) == 1

        new_game = Game.objects.get(id=new_game_id)  
        assert new_game.name == 'Игра'
        assert new_game.genre_fk == gnr
        assert new_game.platform_fk == plt
        assert new_game.developer_fk == dvl

    def test_delete_game(self):
        games=baker.make("Game",10)

        r=self.client.get('/api/games/')
        data=r.json()
        assert len(data)==10

        game_id_to_delete = games[3].id
        self.client.delete(f'/api/games/{game_id_to_delete}/')
        
        r=self.client.get('/api/games/')
        data=r.json()
        assert len(data)==9

        assert game_id_to_delete not in [i['id'] for i in data]

    def test_update_game(self):
        games=baker.make("Game",10)
        game:Game = games[2]

        r=self.client.get(f'/api/games/{game.id}/')
        data = r.json()
        assert data['name'] == game.name


        r=self.client.patch(f'/api/games/{game.id}/',{
            "name":"Ляля",

        })
        assert r.status_code == 200

        r=self.client.get(f'/api/games/{game.id}/')
        data = r.json()
        assert data['name'] == "Ляля"

        game.refresh_from_db()
        assert data['name']==game.name

    def test_create_developer(self):
        cntr = baker.make("CountryDevelop")

        r = self.client.post("/api/developer/", {
            "name": "Разраб",
            "country_fk": cntr.id
        })

        new_developer_id = r.json()['id']

        developers = Developer.objects.all()
        assert len(developers) == 1

        new_developer = Developer.objects.get(id=new_developer_id)  
        assert new_developer.name == 'Разраб'
        assert new_developer.country_fk == cntr


    def test_delete_developer(self):
        developers=baker.make("Developer",10)

        r=self.client.get('/api/developer/')
        data=r.json()
        assert len(data)==10

        developer_id_to_delete = developers[3].id
        self.client.delete(f'/api/developer/{developer_id_to_delete}/')
        
        r=self.client.get('/api/developer/')
        data=r.json()
        assert len(data)==9

        assert developer_id_to_delete not in [i['id'] for i in data]

    def test_update_developer(self):
        developers=baker.make("Developer",10)
        developer:Developer = developers[2]

        r=self.client.get(f'/api/developer/{developer.id}/')
        data = r.json()
        assert data['name'] == developer.name


        r=self.client.patch(f'/api/developer/{developer.id}/',{
            "name":"Ляля",
        })
        assert r.status_code == 200

        r=self.client.get(f'/api/developer/{developer.id}/')
        data = r.json()
        assert data['name'] == "Ляля"

        developer.refresh_from_db()
        assert data['name']==developer.name    

        
