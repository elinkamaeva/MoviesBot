import requests

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
	new_link = link.replace('genre', 'genre=' + str(genre_id)).replace('type', 'type=' + type_) #создаём ссылку
	search_genre = requests.get(new_link, headers=headers_auth)
	search_genre = search_genre.json()
	page_count = search_genre['pagesCount'] #количество доступных страниц фильмов, по 20 фильмов на странице
	answer = 'дальше'

	for i in range(page_count): #цикл создания ссылки по номеру страницы до тех пор, пока не закончатся страницы
		new_link = new_link[:-1] + str(i+1) #создаём нью ссылку
		search_genre = requests.get(new_link, headers=headers_auth)
		search_genre = search_genre.json()
		page_count = search_genre['pagesCount']
		films = search_genre['films']
		j = 0
		
		while answer == 'дальше' and j < len(films) - 2: #цикл вывода фильмов до тех пор, пока список не закончится
			for _ in range(3):
				film1 = films[j]
				film2 = films[j+1]
				film3 = films[j+2]
				
			print(film1, film2, film3) #пока полный вывод фильмов в виде словаря
			j += 3
			answer = input()

user_genre = input()
user_type = input()
print(find_my_genre(user_genre, user_type))
