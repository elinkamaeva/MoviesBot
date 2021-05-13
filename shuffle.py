import telebot
from telebot import types
#from secret import TOKEN
import requests
from random import randint
from dbhelper import init_db
from dbhelper import add_information

URL_AUTH = 'https://api.themoviedb.org/3/authentication/token/new'
HEADERS_AUTH = {'X-API-KEY': 'TOKEN'}

list_of_numbers = []

def find_my_genre(user_genre):
	genre_ids = requests.get('https://kinopoiskapiunofficial.tech/api/v2.1/films/filters', headers=HEADERS_AUTH)
	genre_ids_json = genre_ids.json()['genres']

	for genre in genre_ids_json:
		if genre['genre'] == user_genre:
			genre_id = genre['id']

	link = 'https://kinopoiskapiunofficial.tech/api/v2.1/films/search-by-filters?genre&order=RATING&type=ALL&ratingFrom=0&ratingTo=10&yearFrom=1888&yearTo=2020&page=1'
	new_link = link.replace('genre', f'genre={genre_id}') #создаём ссылку
	search_genre = requests.get(new_link, headers=HEADERS_AUTH)
	search_genre = search_genre.json()
	page_count = search_genre['pagesCount'] #количество доступных страниц фильмов, по 20 фильмов на странице
	
	new_link = new_link.replace('page=1', f'page={page_count}')

	search_rate = requests.get(new_link, headers=HEADERS_AUTH).json()
	last_page_films = len(search_rate['films'])
	number_of_films = (page_count-1) * 20 + last_page_films # количество фильмов
	
	if len(list_of_numbers) == number_of_films: # проверка оставшихся фильмов
		return False, False, False

	number = randint(0, number_of_films-1) # выбор случайного фильма

	if number in list_of_numbers: # проверка, не был ли этот фильм уже показан
		while number in list_of_numbers:
			number = randint(1, number_of_films)

	list_of_numbers.append(number)

	new_page = (number // 20) + 1
	new_link = new_link.replace(new_link[-1], str(new_page)) # создание ссылки с нужной страницей фильма
	print(new_link)
		
	search_genre = requests.get(new_link, headers=HEADERS_AUTH)
	search_genre = search_genre.json()
	films = search_genre['films']
	film = films[number % 20] #находим фильм
	message_film = {'Название': film['nameRu'], 'Год создания': film['year'], 'Рейтинг': film['rating'], 'Страны': film['countries'], 'Жанры': film['genres']}
	text = ''
	
	for m in message_film.items(): #генерируем сообщение бота
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

def find_by_rate(user_rate):
	link = 'https://kinopoiskapiunofficial.tech/api/v2.2/films/top?type=&page=1'
	new_link = link.replace('type=', f'type={user_rate}')
	search_rate = requests.get(new_link, headers=HEADERS_AUTH)
	search_rate = search_rate.json()
	page_count = search_rate['pagesCount'] # количество доступных страниц фильмов, до 20 фильмов на странице
	
	# создание массива с номерами фильмов, чтобы каждый раз выводить фильмы в различном порядке
	if page_count == 13:
		number_of_films = 250
	else:
		number_of_films = 100

	if len(list_of_numbers) == number_of_films:
		return False, False, False

	number = randint(0, number_of_films-1)

	if number in list_of_numbers:
		while number in list_of_numbers:
			number = randint(1, number_of_films)

	list_of_numbers.append(number)

	new_page = int(new_link[-1]) + (number // 20) + 1
	new_link = new_link.replace(new_link[-1], str(new_page))

	search_rate = requests.get(new_link, headers=HEADERS_AUTH)
	search_rate = search_rate.json()
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

GENRES = ['драма', 'комедия', 'ужасы', 'боевик', 'детектив', 'фантастика', 'документальный', 'мультфильм', 'криминал', 'аниме']
RATES = ['ТОП-250 фильмов за всё время', 'ТОП-100 популярных фильмов']
ENG_RATES = {'ТОП-250 фильмов за всё время': 'TOP_250_BEST_FILMS', 'ТОП-100 популярных фильмов': 'TOP_100_POPULAR_FILMS'}

TOKEN = 'TOKEN'
bot = telebot.TeleBot(TOKEN)

init_db()

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
	
movie_id = 0
movie_name = ''

@bot.callback_query_handler(func=lambda c: c.data == 'Приятного просмотра!')
def go_away(callback_query: types.CallbackQuery):
	bot.answer_callback_query(callback_query.id)
	global list_of_numbers
	list_of_numbers = []
	bot.send_message(callback_query.from_user.id, 'Приятного просмотра!')
	user_id = callback_query.from_user.id
	user_name = callback_query.from_user.username
	print(f'Запиши, что пользователь {user_name} с id {user_id} посмотрел фильм "{movie_name}" с id {movie_id}')
	add_information(
		user_id = user_id,
		user_name = user_name,
		movie_id = movie_id,
		movie_name = movie_name
	)

@bot.callback_query_handler(func=lambda c: True)
def callback_inline(c):
	if c.message:
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
			global movie_id
			global movie_name
			films, poster, trailer, movie_id, movie_name = find_my_genre(genre)

			if films == False:
				bot.send_message(c.from_user.id, 'Фильмы закончились :(\nНапиши снова "привет", чтобы выбрать фильмы по другим критериям')

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
			global movie_id
			global movie_name
			films, poster, trailer, movie_id, movie_name = find_by_rate(rate_to_find)

			if films == False:
				bot.send_message(c.from_user.id, 'Фильмы закончились :(\nНапиши снова "привет", чтобы выбрать фильмы по другим критериям')

			else:
				bot.send_message(c.from_user.id, films)
				bot.send_photo(c.from_user.id, poster)
				if trailer != False:
					bot.send_message(c.from_user.id, f'Трейлер фильма:\n{trailer}')
				bot.send_message(c.from_user.id, 'Как вам этот фильм?', reply_markup=markup_data)

USERS = set()

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, 'Чтобы начать, напиши "привет"')

@bot.message_handler(content_types=['text'])
def send_text(message):
	if message.text.lower() == 'привет':
		name = message.from_user.first_name
		bot.send_message(message.chat.id, f'Привет, {name}')
		markup = types.InlineKeyboardMarkup()
		item_genre = types.InlineKeyboardButton('По жанру', callback_data='genre')
		item_rate = types.InlineKeyboardButton('По рейтингу', callback_data='rate')
		item_year = types.InlineKeyboardButton('По году создания', callback_data='year')
		item_country = types.InlineKeyboardButton('По стране создания', callback_data='country')
		i_dont_know = types.InlineKeyboardButton('Я не знаю, что хочу', callback_data='what') #пока не очень понимаю, как это реализовать
		markup.add(item_genre, item_rate, item_year, item_country, i_dont_know)
		bot.send_message(message.chat.id, 'Выберите критерий поиска:', reply_markup=markup)
		USERS.add(message.from_user.id)
		
	elif message.text.lower() == 'пока':
		name = message.from_user.first_name
		bot.send_message(message.chat.id, f'Прощай, создатель {name}')

bot.polling()
