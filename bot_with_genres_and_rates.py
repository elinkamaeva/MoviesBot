import telebot
from telebot import types
#from secret import TOKEN
import requests

URL_AUTH = 'https://api.themoviedb.org/3/authentication/token/new'
headers_auth = {'X-API-KEY': 'bdab7229-245c-48d4-a80c-860085430385'}

def find_my_genre(user_genre, user_type, number):
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
	if (number >= 20) and (int(new_link[-1]) <= page_count):
		new_page = int(new_link[-1]) + (number // 20)
		new_link = new_link.replace('page=' + new_link[-1], f'page={new_page}')
	search_genre = requests.get(new_link, headers=headers_auth)
	search_genre = search_genre.json()
	films = search_genre['films']
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

	return  text, film['posterUrl']

def find_by_rate(user_rate, number):
  link = 'https://kinopoiskapiunofficial.tech/api/v2.2/films/top?type=&page=1'
  new_link = link.replace('type=', f'type={user_rate}')
  search_rate = requests.get(new_link, headers=headers_auth)
  search_rate = search_rate.json()
  page_count = search_rate['pagesCount'] #количество доступных страниц фильмов, по 20 фильмов на странице
  if (number >= 20) and (int(new_link[-1]) <= page_count):
    new_page = int(new_link[-1]) + (number // 20)
    new_link = new_link.replace('page=' + new_link[-1], f'page={new_page}')
  search_rate = requests.get(new_link, headers=headers_auth)
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

  return  text, film['posterUrl']

genres = ['драма', 'комедия', 'ужасы', 'боевик', 'детектив', 'фантастика', 'документальный', 'мультфильм', 'криминал', 'аниме']

bot = telebot.TeleBot('1762716554:AAHSRbHl1BJck-8DMpoXhDCIn9vxi6qMxnc')

@bot.callback_query_handler(func=lambda c: c.data == 'genre')
def process_callback_button1(callback_query: types.CallbackQuery):
	bot.answer_callback_query(callback_query.id)
	markup_genres = types.InlineKeyboardMarkup()
	i = 0
	for g in genres:
		markup_genres.add(types.InlineKeyboardButton(g, callback_data='genres' + str(i)))
		i += 1
	bot.send_message(callback_query.from_user.id, 'Выберите жанр:', reply_markup=markup_genres)
 
@bot.callback_query_handler(func=lambda c: c.data == 'rate')
def process_callback_button1(callback_query: types.CallbackQuery):
	bot.answer_callback_query(callback_query.id)
	markup_rates = types.InlineKeyboardMarkup()
	i = 0
	for r in rates:
		markup_rates.add(types.InlineKeyboardButton(r, callback_data='rates' + str(i)))
		i += 1
	bot.send_message(callback_query.from_user.id, 'Выберите интересующий вас рейтинг', reply_markup=markup_rates)

@bot.callback_query_handler(func=lambda c: c.data == 'Приятного просмотра!')
def go_away(callback_query: types.CallbackQuery):
	bot.answer_callback_query(callback_query.id)
	bot.send_message(callback_query.from_user.id, 'Приятного просмотра!')

j = -1

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
        all = types.InlineKeyboardButton('Хочу смотреть его', callback_data='Приятного просмотра!')
        markup_data.add(again, all)
        global j
        j += 1
        num = int(c.data[-1])
        genre = genres[num]
        films, url = find_my_genre(genre, 'фильм', j)
        bot.send_message(c.from_user.id, films)
        bot.send_photo(c.from_user.id, url)
        bot.send_message(c.from_user.id, 'Как вам этот фильм?', reply_markup=markup_data)
      elif c.data.startswith('rates'):
        num = int(c.data[-1])
        rate = rates[num]
        rate_to_find = eng_rates[rate]
        markup_data = types.InlineKeyboardMarkup()
        again = types.InlineKeyboardButton('Дальше', callback_data=c.data)
        all = types.InlineKeyboardButton('Хочу смотреть его', callback_data='Приятного просмотра!')
        markup_data.add(again, all)
        j += 1
        num = int(c.data[-1])
        films, url = find_by_rate(rate_to_find, j)
        bot.send_message(c.from_user.id, films)
        bot.send_photo(c.from_user.id, url)
        bot.send_message(c.from_user.id, 'Как вам этот фильм?', reply_markup=markup_data)
            
USERS = set()

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Howdy, how are you doing?")

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

# def find_out_rate(message):
	# если выбран фильм
		# def job():
			# markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
			# itembtn1 = types.KeyboardButton('Да')
			# itembtn2 = types.KeyboardButton('Нет')
			# markup.add(itembtn1, itembtn2)
			# bot.send_message(message.chat.id, "Понравился ли Вам фильм?", reply_markup=markup)
			# return schedule.CancelJob
	# now = datetime.now().strftime('%H:%M:%S')
	# schedule.every().day.at(now).do(job)
	# while True:
		# schedule.run_pending()
		# time.sleep(1)

bot.polling()
