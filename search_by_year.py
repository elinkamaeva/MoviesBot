import requests

URL_AUTH = 'https://api.themoviedb.org/3/authentication/token/new'
headers_auth = {'X-API-KEY': 'bdab7229-245c-48d4-a80c-860085430385'}

def find_by_year(user_year, user_type):
	types = {'фильм': 'FILM', 'сериал': 'TV_SHOW', 'любое': 'ALL'}
	type_ = types[user_type]

	min_year = user_year - user_year%10
	max_year = min_year + 10

	link = 'https://kinopoiskapiunofficial.tech/api/v2.1/films/search-by-filters?order=RATING&type&ratingFrom=0&ratingTo=10&yearFrom&yearTo&page=1'
	new_link = link.replace('type', 'type=' + type_)
	new_link = new_link.replace('yearFrom', 'yearFrom=' + str(min_year))
	new_link = new_link.replace('yearTo', 'yearTo=' + str(max_year))

	search_year = requests.get(new_link, headers=headers_auth)
	search_year = search_year.json()
	page_count = search_year['pagesCount']
	answer = 'дальше'

	for i in range(page_count):
		new_link = new_link[:-1] + str(i+1)
		search_year = requests.get(new_link, headers=headers_auth)
		search_year = search_year.json()
		films = search_year['films']
		j = 0
		while answer == 'дальше' and j < len(films) - 2:
			for _ in range(3):
				film1 = films[j]
				film2 = films[j+1]
				film3 = films[j+2]
			print(film1, film2, film3)
			j += 3
			answer = input()

print(find_by_year(1940, 'фильм'))