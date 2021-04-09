import requests
import re

URL_AUTH = 'https://api.themoviedb.org/3/authentication/token/new'
headers_auth = {'X-API-KEY': 'bdab7229-245c-48d4-a80c-860085430385'}

def find_my_genre(user_genre, user_type):
	types = {'фильм': 'FILM', 'сериал': 'TV_SHOW', 'любое': 'ALL'}
	type_ = types[user_type]

	genre_ids = requests.get('https://kinopoiskapiunofficial.tech/api/v2.1/films/filters', headers=headers_auth)
	genre_ids_json = genre_ids.json()['genres']

	for genre in genre_ids_json:
		if genre['genre'] == user_genre:
			genre_id = genre['id']

	link = 'https://kinopoiskapiunofficial.tech/api/v2.1/films/search-by-filters?genre&order=RATING&type&ratingFrom=0&ratingTo=10&yearFrom=1888&yearTo=2020&page=1'
	new_link = link.replace('genre', 'genre=' + str(genre_id)).replace('type', 'type=' + type_)
	search_genre = requests.get(new_link, headers=headers_auth)
	search_genre = search_genre.json()

	print(search_genre)

user_genre = input()
user_type = input()
print(find_my_genre(user_genre, user_type))
