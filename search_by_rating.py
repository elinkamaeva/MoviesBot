import requests

URL_AUTH = 'https://api.themoviedb.org/3/authentication/token/new'
headers_auth = {'X-API-KEY': 'bdab7229-245c-48d4-a80c-860085430385'}

def find_by_country(user_rate, user_type):
	types = {'фильм': 'FILM', 'сериал': 'TV_SHOW', 'любое': 'ALL'}
	type_ = types[user_type]

	min_rate = int(user_rate)
	max_rate = min_rate + 1

	link = 'https://kinopoiskapiunofficial.tech/api/v2.1/films/search-by-filters?&order=RATING&type&ratingFrom&ratingTo&yearFrom=1888&yearTo=2020&page=1'
	new_link = link.replace('ratingFrom', 'ratingFrom=' + str(min_rate)).replace('ratingTo', 'ratingTo=' + str(max_rate)).replace('type', 'type=' + type_)
	search_rate = requests.get(new_link, headers=headers_auth)
	search_rate = search_rate.json()
	page_count = search_rate['pagesCount']
	answer = 'дальше'

	for i in range(page_count):
		new_link = new_link[:-1] + str(i+1)
		search_rate = requests.get(new_link, headers=headers_auth)
		search_rate = search_rate.json()
		films = search_rate['films']
		j = 0
		while answer == 'дальше' and j < len(films) - 2:
			for _ in range(3):
				film1 = films[j]
				film2 = films[j+1]
				film3 = films[j+2]
			print(film1, film2, film3)
			j += 3
			answer = input()

print(find_by_country(9.4, 'фильм'))