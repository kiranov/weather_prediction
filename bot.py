import datetime
import numpy as np
import telebot


# t.me/markov_weather_bot
# api token: 1281314124:AAH9KihH1H3ziKdmKFWv9QBU0XXpLKrFk1g
# vpn_connect: windscribe connect
# windscribe --help

bot = telebot.TeleBot('1281314124:AAH9KihH1H3ziKdmKFWv9QBU0XXpLKrFk1g')

keyboard0 = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
keyboard0.row('Общий прогноз')
keyboard0.row('Прогнозирование температуры')

list1 = ['Ясно', 'Облачно', 'Дождь', 'Снег', 'Переменная обачность', 'Ясно, временами дождь', 'Ясно, временами снег', 'Облачно, дождь', 'Облачно, снег', 'Мокрый снег, дождь']
list2 = ['<-5', '[-5; -2)', '[-2; 2]', '(2; 5]', '>5']

keyboard1 = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
keyboard1.row('Ясно', 'Облачно', 'Дождь')
keyboard1.row('Снег', 'Переменная обачность')
keyboard1.row('Ясно, временами дождь', 'Ясно, временами снег')
keyboard1.row('Облачно, дождь', 'Облачно, снег', 'Мокрый снег, дождь')

keyboard2 = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
keyboard2.row('<-5', '[-5; -2)', '[-2; 2]', '(2; 5]', '>5')


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id,
                     'Привет, я умею делать общий прогноз погоды и предсказывать температуру. Какой прогноз Вы бы хотели получить?',
                     reply_markup=keyboard0)


def calculation1(now, vector, M):
    month = now
    if month == 1:
        result = vector @ M[0]
    elif month == 2:
        result = vector @ M[1]
    elif month == 3:
        result = vector @ M[2]
    elif month == 4:
        result = vector @ M[3]
    elif month == 5:
        result = vector @ M[4]
    elif month == 6:
        result = vector @ M[5]
    elif month == 7:
        result = vector @ M[6]
    elif month == 8:
        result = vector @ M[7]
    elif month == 9:
        result = vector @ M[8]
    elif month == 10:
        result = vector @ M[9]
    elif month == 11:
        result = vector @ M[10]
    elif month == 12:
        result = vector @ M[11]
    return result


def calculation2(now, vector, T):
    month = now
    if month == 1:
        result = vector @ T[0]
    elif month == 2:
        result = vector @ T[1]
    elif month == 3:
        result = vector @ T[2]
    elif month == 4:
        result = vector @ T[3]
    elif month == 5:
        result = vector @ T[4]
    elif month == 6:
        result = vector @ T[5]
    elif month == 7:
        result = vector @ T[6]
    elif month == 8:
        result = vector @ T[7]
    elif month == 9:
        result = vector @ T[8]
    elif month == 10:
        result = vector @ T[9]
    elif month == 11:
        result = vector @ T[10]
    elif month == 12:
        result = vector @ T[11]
    return result


def send_text1(message):
    now = datetime.datetime.now()
    weather_matrix = np.load(open("matrix1.npy","rb"))
    if message.text.lower() == 'ясно':
        vector = np.array([1, 0, 0, 0])
        result = calculation1(now.month, vector, weather_matrix)
        bot.send_message(message.chat.id, str(result))
    elif message.text.lower() == 'облачно':
        vector = np.array([0, 1, 0, 0])
        result = calculation1(now.month, vector, weather_matrix)
        bot.send_message(message.chat.id, str(result))
    elif message.text.lower() == 'дождь':
        vector = np.array([0, 0, 1, 0])
        result = calculation1(now.month, vector, weather_matrix)
        bot.send_message(message.chat.id, str(result))
    elif message.text.lower() == 'снег':
        vector = np.array([0, 0, 0, 1])
        result = calculation1(now.month, vector, weather_matrix)
        bot.send_message(message.chat.id, str(result))
    elif message.text.lower() == 'переменная обачность':
        vector = np.array([0.5, 0.5, 0, 0])
        result = calculation1(now.month, vector, weather_matrix)
        bot.send_message(message.chat.id, str(result))
    elif message.text.lower() == 'ясно, временами дождь':
        vector = np.array([0.5, 0.25, 0.25, 0])
        result = calculation1(now.month, vector, weather_matrix)
        bot.send_message(message.chat.id, str(result))
    elif message.text.lower() == 'ясно, временами снег':
        vector = np.array([0.5, 0.1, 0, 0.4])
        result = calculation1(now.month, vector, weather_matrix)
        bot.send_message(message.chat.id, str(result))
    elif message.text.lower() == 'облачно, дождь':
        vector = np.array([0, 0.5, 0.5, 0])
        result = calculation1(now.month, vector, weather_matrix)
        bot.send_message(message.chat.id, str(result))
    elif message.text.lower() == 'облачно, снег':
        vector = np.array([0, 0.5, 0, 0.5])
        result = calculation1(now.month, vector, weather_matrix)
        bot.send_message(message.chat.id, str(result))
    elif message.text.lower() == 'мокрый снег, дождь':
        vector = np.array([0, 0.2, 0.4, 0.4])
        result = calculation1(now.month, vector, weather_matrix)
        bot.send_message(message.chat.id, str(result))
    bot.send_message(message.chat.id, 'Для получения нового прогноза введите /start')


def send_text2(message):
    now = datetime.datetime.now()
    temp_matrix = np.load(open("matrix2.npy","rb"))
    if message.text.lower() == '<-5':
        vector = np.array([1, 0, 0, 0, 0])
        result = calculation2(now.month, vector, temp_matrix)
        bot.send_message(message.chat.id, str(result))
    elif message.text.lower() == '[-5; -2)':
        vector = np.array([0, 1, 0, 0, 0])
        result = calculation2(now.month, vector, temp_matrix)
        bot.send_message(message.chat.id, str(result))
    elif message.text.lower() == '[-2; 2]':
        vector = np.array([0, 0, 1, 0, 0])
        result = calculation2(now.month, vector, temp_matrix)
        bot.send_message(message.chat.id, str(result))
    elif message.text.lower() == '(2; 5]':
        vector = np.array([0, 0, 0, 1, 0])
        result = calculation2(now.month, vector, temp_matrix)
        bot.send_message(message.chat.id, str(result))
    elif message.text.lower() == '>5':
        vector = np.array([0, 0, 0, 0, 1])
        result = calculation2(now.month, vector, temp_matrix)
        bot.send_message(message.chat.id, str(result))
    bot.send_message(message.chat.id, 'Для получения нового прогноза введите /start')


@bot.message_handler(content_types=['text'])
def type_predction(message):
    if message.text.lower() == 'общий прогноз':
        bot.send_message(message.chat.id, 'Чтобы узнать погоду в Долгопрудном на завтра, мне нужно знать сегодняшнюю. Для ее описания выберете наиболее подходящий вариант',
                         reply_markup=keyboard1)
    elif message.text.lower() == 'прогнозирование температуры':
        bot.send_message(message.chat.id, 'Чтобы узнать погоду в Долгопрудном на завтра, мне нужно знать сегодняшнюю. Для ее описания выберете наиболее подходящий вариант',
                         reply_markup=keyboard2)
    elif message.text in list1:
        send_text1(message)
    elif message.text in list2:
        send_text2(message)


bot.polling()
