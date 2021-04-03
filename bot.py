import telebot
from telebot import types
import secret

bot = telebot.TeleBot(TOKEN)

@bot.callback_query_handler(func=lambda c: c.data == 'genre')
def process_callback_button1(callback_query: types.CallbackQuery):
	bot.answer_callback_query(callback_query.id)
	genres = ['драма', 'комедия', 'хоррор']
	markup_genres = types.InlineKeyboardMarkup()
	for g in genres:
		markup_genres.add(types.InlineKeyboardButton(g, callback_data='shit'))
	bot.send_message(callback_query.from_user.id, 'Выберите жанр:', reply_markup=markup_genres)

@bot.callback_query_handler(func=lambda c: c.data == 'rate')
def process_callback_button1(callback_query: types.CallbackQuery):
	bot.answer_callback_query(callback_query.id)
	rates = ['ТОП-10', 'ТОП-25', 'ТОП-100']
	markup_rates = types.InlineKeyboardMarkup()
	for r in rates:
		markup_rates.add(types.InlineKeyboardButton(r, callback_data='shit'))
	bot.send_message(callback_query.from_user.id, 'Выставите интересующий вас рейтинг', reply_markup=markup_rates)

@bot.callback_query_handler(func=lambda c: c.data == 'year')
def process_callback_button1(callback_query: types.CallbackQuery):
	bot.answer_callback_query(callback_query.id)
	bot.send_message(callback_query.from_user.id, 'Введите интересующий вас год')

@bot.callback_query_handler(func=lambda c: c.data == 'country')
def process_callback_button1(callback_query: types.CallbackQuery):
	bot.answer_callback_query(callback_query.id)
	bot.send_message(callback_query.from_user.id, 'Введите название интересующей вас страны')

USERS = set()

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(content_types=['text'])
def send_text(message):
	if message.text.lower() == 'привет':
		name = message.from_user.first_name
		bot.send_message(message.chat.id, f'Привет, {name}')
		if message.from_user.id in USERS:
			markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
			itembtn1 = types.KeyboardButton('Да')
			itembtn2 = types.KeyboardButton('Нет')
			markup.add(itembtn1, itembtn2)
			bot.send_message(message.chat.id, "Понравился ли Вам фильм?", reply_markup=markup)
		markup = types.InlineKeyboardMarkup()
		item_genre = types.InlineKeyboardButton('По жанру', callback_data='genre')
		item_rate = types.InlineKeyboardButton('По рейтингу', callback_data='rate')
		item_year = types.InlineKeyboardButton('По году создания', callback_data='year')
		item_country = types.InlineKeyboardButton('По стране создания', callback_data='country')
		markup.add(item_genre, item_rate, item_year, item_country)
		bot.send_message(message.chat.id, 'Выберите критерий поиска:', reply_markup=markup)
		USERS.add(message.from_user.id)
	elif message.text.lower() == 'пока':
		name = message.from_user.first_name
		bot.send_message(message.chat.id, 'Прощай, создатель ' + name)

bot.polling()
