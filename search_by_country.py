import requests

URL_AUTH = 'https://api.themoviedb.org/3/authentication/token/new'
headers_auth = {'X-API-KEY': 'bdab7229-245c-48d4-a80c-860085430385'}

def find_by_country(user_country, user_type):
	types = {'фильм': 'FILM', 'сериал': 'TV_SHOW', 'любое': 'ALL'}
	type_ = types[user_type]

	country_ids = requests.get('https://kinopoiskapiunofficial.tech/api/v2.1/films/filters', headers=headers_auth)
	country_ids_json = country_ids.json()['countries']

	for country in country_ids_json:
		if country['country'] == user_country:
			country_id = country['id']

	link = 'https://kinopoiskapiunofficial.tech/api/v2.1/films/search-by-filters?country&order=RATING&type&ratingFrom=0&ratingTo=10&yearFrom=1888&yearTo=2020&page=1'
	new_link = link.replace('country', 'country=' + str(country_id)).replace('type', 'type=' + type_)
	search_country = requests.get(new_link, headers=headers_auth)
	search_country = search_country.json()
	page_count = search_country['pagesCount']
	answer = 'дальше'

	for i in range(page_count):
		new_link = new_link[:-1] + str(i+1)
		search_country = requests.get(new_link, headers=headers_auth)
		search_country = search_country.json()
		films = search_country['films']
		j = 0
		while answer == 'дальше' and j < len(films) - 2:
			for _ in range(3):
				film1 = films[j]
				film2 = films[j+1]
				film3 = films[j+2]
			print(film1, film2, film3)
			j += 3
			answer = input()

print(find_by_country('Великобритания', 'фильм'))