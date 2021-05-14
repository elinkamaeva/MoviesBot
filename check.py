import telebot
from telebot import types
import requests
from random import randint
from dbhelper import init_db
from dbhelper import add_information
from dbhelper import add_similar
from dbhelper import get_movies_ids
from dbhelper import delete_movie

URL_AUTH = 'https://api.themoviedb.org/3/authentication/token/new'
HEADERS_AUTH = {'X-API-KEY': 'bdab7229-245c-48d4-a80c-860085430385'}

list_of_numbers = []

# поиск фильмов по жанру
def find_my_genre(user_genre):
	genre_ids = requests.get('https://kinopoiskapiunofficial.tech/api/v2.1/films/filters', headers=HEADERS_AUTH)
	genre_ids_json = genre_ids.json()['genres']

	for genre in genre_ids_json:
		if genre['genre'] == user_genre:
			genre_id = genre['id']

	link = 'https://kinopoiskapiunofficial.tech/api/v2.1/films/search-by-filters?genre&order=RATING&type=ALL&ratingFrom=0&ratingTo=10&yearFrom=1888&yearTo=2020&page=1'
	# создание ссылки
	new_link = link.replace('genre', f'genre={genre_id}')
	search_genre = requests.get(new_link, headers=HEADERS_AUTH).json()
	page_count = search_genre['pagesCount'] # количество доступных страниц фильмов, по 20 фильмов на странице
	new_link = new_link.replace('page=1', f'page={page_count}')

	search_genre = requests.get(new_link, headers=HEADERS_AUTH).json()
	last_page_films = len(search_genre['films'])
	number_of_films = (page_count - 1) * 20 + last_page_films # количество подходящих фильмов
	
	# проверка оставшихся фильмов
	if len(list_of_numbers) == number_of_films:
		return False, False, False

	number = randint(0, number_of_films - 1) # выбор случайного фильма

	# проверка на то, не был ли этот фильм уже показан
	if number in list_of_numbers:
		while number in list_of_numbers:
			number = randint(1, number_of_films)

	list_of_numbers.append(number)

	new_page = (number // 20) + 1
	new_link = f'{new_link[:-1]}{(new_page)}' # создание ссылки с нужной страницей фильма
		
	search_genre = requests.get(new_link, headers=HEADERS_AUTH).json()
	films = search_genre['films']
	film = films[number % 20] # нужный фильм
	message_film = {'Название': film['nameRu'], 'Год создания': film['year'], 'Рейтинг': film['rating'], 'Страны': film['countries'], 'Жанры': film['genres']}
	text = ''
	
	# формирование сообщение бота
	for m in message_film.items():
		if type(m[1]) == list:
			list_values = []
			for c in m[1]:
				list_values.append(list(c.values())[0])
			values = ', '.join(list_values)
			text += f'{m[0]}: {values}' + '\n'
		else:
			text += f'{m[0]}: {m[1]}' + '\n'

	film_id = film['filmId']
	film_name = film['nameRu']
	link_trailer = f'https://kinopoiskapiunofficial.tech/api/v2.1/films/{film_id}/videos'
	get_trailer = requests.get(link_trailer, headers=HEADERS_AUTH)
	get_trailer = get_trailer.json()

	if len(get_trailer['trailers']) != 0:
		return text, film['posterUrl'], get_trailer['trailers'][0]['url'], film_id, film_name

	else: 
		return text, film['posterUrl'], False, film_id, film_name

# поиск фильмов по рейтингу
def find_by_rate(user_rate):
	link = 'https://kinopoiskapiunofficial.tech/api/v2.2/films/top?type=&page=1'
	new_link = link.replace('type=', f'type={user_rate}')
	search_rate = requests.get(new_link, headers=HEADERS_AUTH).json()
	page_count = search_rate['pagesCount']
	
	# создание массива с номерами фильмов, чтобы каждый раз выводить фильмы в различном порядке
	if page_count == 13:
		number_of_films = 250
	else:
		number_of_films = 100

	if len(list_of_numbers) == number_of_films:
		return False, False, False

	number = randint(0, number_of_films - 1)

	if number in list_of_numbers:
		while number in list_of_numbers:
			number = randint(1, number_of_films)

	list_of_numbers.append(number)

	new_page = (number // 20) + 1
	new_link = f'{new_link[:-1]}{(new_page)}'

	search_rate = requests.get(new_link, headers=HEADERS_AUTH).json()
	films = search_rate['films']
	film = films[number % 20]
	message_film = {'Название': film['nameRu'], 'Год создания': film['year'], 'Рейтинг': film['rating'], 'Страны': film['countries'], 'Жанры': film['genres']}
	text = ''

	for m in message_film.items():
		if type(m[1]) == list:
			list_values = []
			for c in m[1]:
				list_values.append(list(c.values())[0])
			values = ', '.join(list_values)
			text += f'{m[0]}: {values}' + '\n'
		else:
		  	text += f'{m[0]}: {m[1]}' + '\n'

	film_id = film['filmId']
	film_name = film['nameRu']
	link_trailer = f'https://kinopoiskapiunofficial.tech/api/v2.1/films/{film_id}/videos'
	get_trailer = requests.get(link_trailer, headers=HEADERS_AUTH)
	get_trailer = get_trailer.json()

	if len(get_trailer['trailers']) != 0:
		return text, film['posterUrl'], get_trailer['trailers'][0]['url'], film_id, film_name

	else: 
		return text, film['posterUrl'], False, film_id, film_name
    
# поиск фильмов по году создания
def find_by_year(user_year):
	year_from = ''
	for i in range(4):
		year_from += user_year[i]
	year_to = ''
	for i in range(5, 9):
		year_to += user_year[i]
    
	link = 'https://kinopoiskapiunofficial.tech/api/v2.1/films/search-by-filters?order=RATING&type=ALL&ratingFrom=0&ratingTo=10&yearFrom=1888&yearTo=2020&page=1'
	new_link = link.replace('yearFrom=1900', f'yearFrom={year_from}')
	new_link = new_link.replace('yearTo=2020', f'yearTo={year_to}')
    
	search_year = requests.get(new_link, headers=HEADERS_AUTH).json()
	page_count = search_year['pagesCount']    
	new_link = new_link.replace('page=1', f'page={page_count}')
    
	search_rate = requests.get(new_link, headers=HEADERS_AUTH).json()
	last_page_films = len(search_rate['films'])
	number_of_films = (page_count - 1) * 20 + last_page_films
    
	if len(list_of_numbers) == number_of_films:
		return False, False, False
    
	number = randint(0, number_of_films - 1)
    
	if number in list_of_numbers:
		while number in list_of_numbers:
			number = randint(1, number_of_films)

	list_of_numbers.append(number)

	new_page = (number // 20) + 1
	new_link = f'{new_link[:-1]}{(new_page)}'
		
	search_year = requests.get(new_link, headers=HEADERS_AUTH).json()
	films = search_year['films']
	film = films[number % 20]
	message_film = {'Название': film['nameRu'], 'Год создания': film['year'], 'Рейтинг': film['rating'], 'Страны': film['countries'], 'Жанры': film['genres']}
	text = ''
    
	for m in message_film.items():
		if type(m[1]) == list:
			list_values = []
			for c in m[1]:
				list_values.append(list(c.values())[0])
			values = ', '.join(list_values)
			text += f'{m[0]}: {values}' + '\n'
		else:
			text += f'{m[0]}: {m[1]}' + '\n'
            
	film_id = film['filmId']
	film_name = film['nameRu']
	link_trailer = f'https://kinopoiskapiunofficial.tech/api/v2.1/films/{film_id}/videos'
	get_trailer = requests.get(link_trailer, headers=HEADERS_AUTH)
	get_trailer = get_trailer.json()
    
	if len(get_trailer['trailers']) != 0:
		return text, film['posterUrl'], get_trailer['trailers'][0]['url'], film_id, film_name

	else: 
		return text, film['posterUrl'], False, film_id, film_name
    
# поиск фильмов по стране создания
def find_by_country(user_country):
	country_ids = requests.get('https://kinopoiskapiunofficial.tech/api/v2.1/films/filters', headers=HEADERS_AUTH)
	country_ids_json = country_ids.json()['countries']
    
	for country in country_ids_json:
		if country['country'] == user_country:
			country_id = country['id']
            
	link = 'https://kinopoiskapiunofficial.tech/api/v2.1/films/search-by-filters?country&order=RATING&type=ALL&ratingFrom=0&ratingTo=10&yearFrom=1888&yearTo=2020&page=1'
	new_link = link.replace('country', f'country={country_id}')
	search_country = requests.get(new_link, headers=HEADERS_AUTH).json()
	page_count = search_country['pagesCount']
	new_link = new_link.replace('page=1', f'page={page_count}')
    
	search_rate = requests.get(new_link, headers=HEADERS_AUTH).json()
	last_page_films = len(search_rate['films'])
	number_of_films = (page_count - 1) * 20 + last_page_films
    
	if len(list_of_numbers) == number_of_films: 
		return False, False, False
    
	number = randint(0, number_of_films - 1)
    
	if number in list_of_numbers: 
		while number in list_of_numbers:
			number = randint(1, number_of_films)
    
	list_of_numbers.append(number)
    
	new_page = (number // 20) + 1
	new_link = f'{new_link[:-1]}{(new_page)}'
    
	search_country = requests.get(new_link, headers=HEADERS_AUTH).json()
	films = search_country['films']
	film = films[number % 20]
	message_film = {'Название': film['nameRu'], 'Год создания': film['year'], 'Рейтинг': film['rating'], 'Страны': film['countries'], 'Жанры': film['genres']}
	text = ''
    
	for m in message_film.items():
		if type(m[1]) == list:
			list_values = []
			for c in m[1]:
				list_values.append(list(c.values())[0])
			values = ', '.join(list_values)
			text += f'{m[0]}: {values}' + '\n'
		else:
			text += f'{m[0]}: {m[1]}' + '\n'
    
	film_id = film['filmId']
	film_name = film['nameRu']
	link_trailer = f'https://kinopoiskapiunofficial.tech/api/v2.1/films/{film_id}/videos'
	get_trailer = requests.get(link_trailer, headers=HEADERS_AUTH)
	get_trailer = get_trailer.json()
    
	if len(get_trailer['trailers']) != 0:
		return text, film['posterUrl'], get_trailer['trailers'][0]['url'], film_id, film_name

	else: 
		return text, film['posterUrl'], False, film_id, film_name
	
# поиск фильмов по истории просмотров
def get_recommendation(user_id):
	lst = get_movies_ids(user_id=user_id)
	number_of_movies = len(lst)

	if number_of_movies == 0:
		text = 'К сожалению, для Вас эта функция еще не доступна.\nПодберите хотя бы один фильм по любому другому критерию поиска'
		return text, False, False, False, False

	elif len(list_of_numbers) == number_of_movies:
		return False, False, False, False, False
	
	number = randint(0, number_of_movies - 1)

	if number in list_of_numbers:
		while number in list_of_numbers:
			number = randint(1, number_of_movies)
		
	list_of_numbers.append(number)
	
	movie_id = lst[number][0]
	get_information = requests.get(f'https://kinopoiskapiunofficial.tech/api/v2.1/films/{movie_id}',
                                   headers=HEADERS_AUTH)
	movie_information = get_information.json()['data']
	message = {'Название': movie_information['nameRu'], 'Год создания': movie_information['year'],
               'Страны': movie_information['countries'], 'Жанры': movie_information['genres']}

	text = ''
        
	for m in message.items():
		if type(m[1]) == list:
			list_values = []
			for c in m[1]:
				list_values.append(list(c.values())[0])
			values = ', '.join(list_values)
			text += f'{m[0]}: {values}' + '\n'
		else:
			text += f'{m[0]}: {m[1]}' + '\n'
		
	link_trailer = f'https://kinopoiskapiunofficial.tech/api/v2.1/films/{movie_id}/videos'
	get_trailer = requests.get(link_trailer, headers=HEADERS_AUTH)
	get_trailer = get_trailer.json()

	if len(get_trailer['trailers']) != 0:
		return text, movie_information['posterUrl'], get_trailer['trailers'][0]['url'], movie_id, movie_information['nameRu']

	else:
		return text, movie_information['posterUrl'], False, movie_id, movie_information['nameRu']

GENRES = ['драма', 'комедия', 'ужасы', 'боевик', 'детектив', 'фантастика', 'документальный', 'мультфильм', 'криминал', 'аниме']
RATES = ['ТОП-250 фильмов за всё время', 'ТОП-100 популярных фильмов']
ENG_RATES = {'ТОП-250 фильмов за всё время': 'TOP_250_BEST_FILMS', 'ТОП-100 популярных фильмов': 'TOP_100_POPULAR_FILMS'}
YEARS = ['1888-1899', '1900-1919', '1920-1939', '1940-1959', '1960-1979', '1980-1999', '2000-2009', '2010-2020']
COUNTRIES = ['США', 'Россия', 'СССР', 'Германия', 'Великобритания', 'Франция', 'Италия', 'Япония', 'Бразилия', 'Австралия']

# далее функции для работы самого бота
TOKEN = '1762716554:AAHSRbHl1BJck-8DMpoXhDCIn9vxi6qMxnc'
bot = telebot.TeleBot(TOKEN)

init_db()

movie_id = 0
movie_name = ''

@bot.callback_query_handler(func=lambda c: c.data == 'genre')
def process_callback_button1(callback_query: types.CallbackQuery):
	bot.answer_callback_query(callback_query.id)
	markup_genres = types.InlineKeyboardMarkup()
	i = 0
	for g in GENRES:
		markup_genres.add(types.InlineKeyboardButton(g, callback_data=f'genres{i}'))
		i += 1
	bot.send_message(callback_query.from_user.id, 'Выберите жанр:', reply_markup=markup_genres)
 
@bot.callback_query_handler(func=lambda c: c.data == 'rate')
def process_callback_button1(callback_query: types.CallbackQuery):
	bot.answer_callback_query(callback_query.id)
	markup_rates = types.InlineKeyboardMarkup()
	i = 0
	for r in RATES:
		markup_rates.add(types.InlineKeyboardButton(r, callback_data=f'rates{i}'))
		i += 1
	bot.send_message(callback_query.from_user.id, 'Выберите интересующий вас рейтинг', reply_markup=markup_rates)

@bot.callback_query_handler(func=lambda c: c.data == 'year')
def process_callback_button1(callback_query: types.CallbackQuery):
	bot.answer_callback_query(callback_query.id)
	markup_years = types.InlineKeyboardMarkup()
	i = 0
	for y in YEARS:
		markup_years.add(types.InlineKeyboardButton(y, callback_data=f'years{i}'))
		i += 1
	bot.send_message(callback_query.from_user.id, 'Выберите год создания', reply_markup=markup_years)

@bot.callback_query_handler(func=lambda c: c.data == 'country')
def process_callback_button1(callback_query: types.CallbackQuery):
	bot.answer_callback_query(callback_query.id)
	markup_countries = types.InlineKeyboardMarkup()
	i = 0
	for c in COUNTRIES:
		markup_countries.add(types.InlineKeyboardButton(c, callback_data=f'countries{i}'))
		i += 1
	bot.send_message(callback_query.from_user.id, 'Выберите страну создания', reply_markup=markup_countries)

@bot.callback_query_handler(func=lambda c: c.data == 'Приятного просмотра!')
def go_away(callback_query: types.CallbackQuery):
	bot.answer_callback_query(callback_query.id)
	global list_of_numbers
	global movie_id
	global movie_name
	list_of_numbers = []
	bot.send_message(callback_query.from_user.id, 'Приятного просмотра!')
	user_id = callback_query.from_user.id
	user_name = callback_query.from_user.username
	add_information(
		user_id = user_id,
		user_name = user_name,
		movie_id = movie_id,
		movie_name = movie_name
	)
	l = get_movies_ids(user_id=user_id)
	for i in l:
		if i[0] == movie_id:
			delete_movie(
				user_id=user_id,
				movie_id=movie_id
			)
	link_similars = f'https://kinopoiskapiunofficial.tech//api/v2.2/films/{movie_id}/similars'
	get_similars = requests.get(link_similars, headers=HEADERS_AUTH)
	get_similars = get_similars.json()
	if len(get_similars['items']) != 0:
		for item in get_similars['items']:
			movie_id = item['filmId']
			movie_name = item['nameRu']
			count = 0
			for i in l:
				if movie_id != i[0]: # проверка на то, нет ли данного фильма в рекомендованных пользователю фильмах
					count += 1
			if count == len(l):
				add_similar(
					user_id=user_id,
					user_name=user_name,
					movie_id=movie_id,
					movie_name=movie_name
				)

def choose_criterion(where, who):
	markup = types.InlineKeyboardMarkup(row_width=1)
	item_genre = types.InlineKeyboardButton('По жанру', callback_data='genre')
	item_rate = types.InlineKeyboardButton('По рейтингу', callback_data='rate')
	item_year = types.InlineKeyboardButton('По году создания', callback_data='year')
	item_country = types.InlineKeyboardButton('По стране создания', callback_data='country')
	i_dont_know = types.InlineKeyboardButton('Я не знаю, что хочу', callback_data='what')
	markup.add(item_genre, item_rate, item_year, item_country, i_dont_know)
	bot.send_message(where, 'Выберите критерий поиска:', reply_markup=markup)
	USERS.add(who)				
				
@bot.callback_query_handler(func=lambda c: c.data == 'what')
def process_callback_button1(callback_query: types.CallbackQuery):
	bot.answer_callback_query(callback_query.id)
	global movie_id
	global movie_name
	text, poster, trailer, movie_id, movie_name = get_recommendation(callback_query.from_user.id)
	if text != False:
		bot.send_message(callback_query.from_user.id, text)
	else:
		bot.send_message(callback_query.from_user.id, 'Фильмы закончились :(\nПопробуй выбрать фильмы по другим критериям')
		choose_criterion(callback_query.from_user.id, callback_query.from_user.id)
	if poster != False:
		bot.send_photo(callback_query.from_user.id, poster)
	if trailer != False:
		bot.send_message(callback_query.from_user.id, f'Трейлер фильма:\n{trailer}')
	if movie_id != False:
		markup_data = types.InlineKeyboardMarkup(row_width=1)
		again = types.InlineKeyboardButton('Дальше', callback_data='what')
		all_ = types.InlineKeyboardButton('Хочу смотреть его', callback_data='Приятного просмотра!')
		markup_data.add(again, all_)
		bot.send_message(callback_query.from_user.id, 'Как вам этот фильм?', reply_markup=markup_data)
	else:
		choose_criterion(callback_query.from_user.id, callback_query.from_user.id)			
				
@bot.callback_query_handler(func=lambda c: True)
def callback_inline(c):
	if c.message:
		global movie_id
		global movie_name
		if c.data.startswith('mood'):
			num = c.data[-1]
			f = films_mood.keys()[num]
			genres_mood = films_mood[f]
			bot.send_message(c.from_user.id, num)

		elif c.data.startswith('genres'):
			markup_data = types.InlineKeyboardMarkup()
			again = types.InlineKeyboardButton('Дальше', callback_data=c.data)
			all_ = types.InlineKeyboardButton('Хочу смотреть его', callback_data='Приятного просмотра!')
			markup_data.add(again, all_)
			num = int(c.data[-1])
			genre = GENRES[num]
			films, poster, trailer, movie_id, movie_name = find_my_genre(genre)

			if films == False:
				bot.send_message(c.from_user.id, 'Фильмы закончились :(\nПопробуй выбрать фильмы по другим критериям')
				choose_criterion(c.from_user.id, c.from_user.id)

			else:
				bot.send_message(c.from_user.id, films)
				bot.send_photo(c.from_user.id, poster)
				if trailer != False:
					bot.send_message(c.from_user.id, f'Трейлер фильма:\n{trailer}')
				bot.send_message(c.from_user.id, 'Как вам этот фильм?', reply_markup=markup_data)

		elif c.data.startswith('rates'):
			num = int(c.data[-1])
			rate = RATES[num]
			rate_to_find = ENG_RATES[rate]
			markup_data = types.InlineKeyboardMarkup()
			again = types.InlineKeyboardButton('Дальше', callback_data=c.data)
			all_ = types.InlineKeyboardButton('Хочу смотреть его', callback_data='Приятного просмотра!')
			markup_data.add(again, all_)
			films, poster, trailer, movie_id, movie_name = find_by_rate(rate_to_find)

			if films == False:
				bot.send_message(c.from_user.id, 'Фильмы закончились :(\nПопробуй выбрать фильмы по другим критериям')
				choose_criterion(c.from_user.id, c.from_user.id)

			else:
				bot.send_message(c.from_user.id, films)
				bot.send_photo(c.from_user.id, poster)
				if trailer != False:
					bot.send_message(c.from_user.id, f'Трейлер фильма:\n{trailer}')
				bot.send_message(c.from_user.id, 'Как вам этот фильм?', reply_markup=markup_data)

		elif c.data.startswith('years'):
			markup_data = types.InlineKeyboardMarkup()
			again = types.InlineKeyboardButton('Дальше', callback_data=c.data)
			all_ = types.InlineKeyboardButton('Хочу смотреть его', callback_data='Приятного просмотра!')
			markup_data.add(again, all_)
			num = int(c.data[-1])
			year = YEARS[num]
			films, poster, trailer, movie_id, movie_name = find_by_year(year)
    
			if films == False:
				bot.send_message(c.from_user.id, 'Фильмы закончились :(\nПопробуй выбрать фильмы по другим критериям')
				choose_criterion(c.from_user.id, c.from_user.id)
        
			else:
				bot.send_message(c.from_user.id, films)
				bot.send_photo(c.from_user.id, poster)
				if trailer != False:
					bot.send_message(c.from_user.id, f'Трейлер фильма:\n{trailer}')
				bot.send_message(c.from_user.id, 'Как вам этот фильм?', reply_markup=markup_data)           

		elif c.data.startswith('countries'):
			markup_data = types.InlineKeyboardMarkup()
			again = types.InlineKeyboardButton('Дальше', callback_data=c.data)
			all_ = types.InlineKeyboardButton('Хочу смотреть его', callback_data='Приятного просмотра!')
			markup_data.add(again, all_)
			num = int(c.data[-1])
			country = COUNTRIES[num]
			films, poster, trailer, movie_id, movie_name = find_by_country(country)
    
			if films == False:
				bot.send_message(c.from_user.id, 'Фильмы закончились :(\nПопробуй выбрать фильмы по другим критериям')
				choose_criterion(c.from_user.id, c.from_user.id)
        
			else:
				bot.send_message(c.from_user.id, films)
				bot.send_photo(c.from_user.id, poster)
				if trailer != False:
					bot.send_message(c.from_user.id, f'Трейлер фильма:\n{trailer}')
				bot.send_message(c.from_user.id, 'Как вам этот фильм?', reply_markup=markup_data)

USERS = set()

@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.reply_to(message, '''Чтобы начать, напишите "привет".
Чтобы узнать, что делает наш бот, нажмите /help''')

@bot.message_handler(commands=['help'])
def send_welcome(message):
	bot.reply_to(message, '''Привет! Вы используете бот MoviesBot.
Здесь Вы можете найти фильм в зависимостиот жанра, рейтинга,года создания,страны создания.
Каждый выбранный фильм будет сохраняться в список Ваших просмотренных фильмов, на основе которых будет формироваться список предложений.
Чтобы посмотреть предложенные фильмы нажмите кнопку "Я не знаю, что хочу".
Для начала напиши боту "привет"''')
	
@bot.message_handler(content_types=['text'])
def send_text(message):
	if message.text.lower() == 'привет':
		name = message.from_user.first_name
		bot.send_message(message.chat.id, f'Привет, {name}')
		choose_criterion(message.chat.id, message.from_user.id)	
	elif message.text.lower() == 'пока':
		name = message.from_user.first_name
		bot.send_message(message.chat.id, f'Прощай, создатель {name}')

bot.polling()
