from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Artist, Movie
from .serializers import ArtistSerializer, MovieDetailSerializer


class ArtistViewSetTest(APITestCase):
    def setUp(self):
        # Create some artists
        self.artist1 = Artist.objects.create(name="Leonardo DiCaprio", country="US", birth_date="1974-11-11")
        self.artist2 = Artist.objects.create(name="Christopher Nolan", country="GB", birth_date="1970-07-30")

        # Create a movie and assign roles
        self.movie = Movie.objects.create(title="Inception", year=2010, director=self.artist2)
        self.movie.actors.add(self.artist1)

    def test_list_artists(self):
        response = self.client.get(reverse('artists-list'))
        artists = Artist.objects.all()
        serializer = ArtistSerializer(artists, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], serializer.data)

    def test_search_artists(self):
        response = self.client.get(reverse('artists-list'), {'search': 'Leonardo'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data['results']
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['name'], "Leonardo DiCaprio")

    def test_filter_artists_by_role_actor(self):
        response = self.client.get(reverse('artists-list'), {'role': 'actor'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data['results']
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['name'], "Leonardo DiCaprio")

    def test_filter_artists_by_role_director(self):
        response = self.client.get(reverse('artists-list'), {'role': 'director'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data['results']
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['name'], "Christopher Nolan")


class MovieViewSetTest(APITestCase):
    def setUp(self):
        # Create some artists
        self.artist1 = Artist.objects.create(name="Leonardo DiCaprio", country="US", birth_date="1974-11-11")
        self.artist2 = Artist.objects.create(name="Christopher Nolan", country="GB", birth_date="1970-07-30")

        # Create a movie
        self.movie = Movie.objects.create(title="Inception", year=2010, director=self.artist2)
        self.movie.actors.add(self.artist1)

    def test_list_movies(self):
        response = self.client.get(reverse('movies-list'))
        movies = Movie.objects.all().select_related('director').prefetch_related('actors')
        serializer = MovieDetailSerializer(movies, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], serializer.data)

    def test_search_movies(self):
        response = self.client.get(reverse('movies-list'), {'search': 'Inception'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], "Inception")

    def test_create_movie(self):
        data = {
            "title": "The Dark Knight",
            "year": 2008,
            "director": self.artist2.id,
            "actors": [self.artist1.id]
        }
        response = self.client.post(reverse('movies-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        movie = Movie.objects.get(title="The Dark Knight")
        self.assertEqual(movie.director, self.artist2)
        self.assertEqual(movie.actors.count(), 1)
        self.assertEqual(movie.actors.first(), self.artist1)

    def test_update_movie(self):
        data = {
            "title": "Inception Updated",
            "year": 2011,
            "director": self.artist2.id,
            "actors": [self.artist1.id]
        }
        response = self.client.put(reverse('movies-detail', kwargs={'pk': self.movie.id}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.movie.refresh_from_db()
        self.assertEqual(self.movie.title, "Inception Updated")
        self.assertEqual(self.movie.year, 2011)

    def test_partial_update_movie(self):
        data = {
            "title": "Inception Partial Update"
        }
        response = self.client.patch(reverse('movies-detail', kwargs={'pk': self.movie.id}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.movie.refresh_from_db()
        self.assertEqual(self.movie.title, "Inception Partial Update")

    def test_delete_movie(self):
        response = self.client.delete(reverse('movies-detail', kwargs={'pk': self.movie.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Movie.objects.filter(pk=self.movie.id).exists())
