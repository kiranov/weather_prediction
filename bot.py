import datetime
import numpy as np
import telebot
import requests
import csv
import collections
import pandas as pd


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


def preprocessing(data):
    processing_data = data
    for i in processing_data:
        if i[2] in {'Thundery outbreaks possible','Moderate rain',
                    'Light drizzle','Light freezing rain','Moderate or heavy rain shower',
                    'Patchy rain possible','Light rain shower','Patchy light drizzle',
                    'Light rain','Moderate or heavy rain with thunder',
                    'Moderate rain at times', 'Heavy rain','Patchy light rain',
                    'Patchy light rain with thunder'}:
            i[2] = 2
        elif i[2] in {'Light snow','Patchy moderate snow','Heavy freezing drizzle',
                      'Moderate snow', 'Heavy snow', 'Light snow showers',
                      'Moderate or heavy sleet', 'Moderate or heavy snow showers',
                      'Light sleet','Light sleet showers','Patchy snow possible',
                      'Blizzard','Patchy heavy snow','Patchy light snow'}:
            i[2] = 3
        elif i[2] in {'Fog','Overcast','Freezing fog','Mist','Partly cloudy'}:
            i[2] = 1
        else:
            i[2] = 0
    return processing_data


def get_weather(now):
    CSV_URL1 = 'http://api.worldweatheronline.com/premium/v1/past-weather.ashx?q=Moscow&date='
    time1 = str(now.year) + '-' + str(now.month) + '-' + str(now.day-1)
    CSV_URL2 = '&enddate='
    time2 = str(now.year) + '-' + str(now.month) + '-' + str(now.day)
    CSV_URL3 = '&key=17c1ea07d59e414eafb80816200105&format=csv&tp=3'
    CSV_URL = CSV_URL1 + time1 + CSV_URL2 + time2 + CSV_URL3
    with requests.Session() as s:
        download = s.get(CSV_URL)
        decoded_content = download.content.decode('utf-8')
        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        my_list = list(cr)
    data = my_list
    counter = collections.defaultdict(int)
    maximum = 0
    for row in data:
        counter[row[0]] += 1
        if counter[row[0]] > maximum:
            maximum = counter[row[0]]
    handle = open("weather_now.csv", 'w')
    writer = csv.writer(handle)
    for row in data:
        if counter[row[0]] >= maximum:
            writer.writerow(row)
    handle.close()
    cols = ['date',
            'time',
            'tempC',
            'tempF',
            'windspeedMiles',
            'windspeedKmph',
            'winddirdegree',
            'winddir16point',
            'weatherCode',
            'weatherIconUrl',
            'weatherDesc',
            'precipMM',
            'precipInches',
            'humidity',
            'visibilityKm',
            'visibilityMiles',
            'pressureMB',
            'pressureInches',
            'cloudcover',
            'HeatIndexC',
            'HeatIndexF',
            'DewPointC',
            'DewPointF',
            'WindChillC',
            'WindChillF',
            'WindGustMiles',
            'WindGustKmph',
            'FeelsLikeC',
            'FeelsLikeF']
    data_now = pd.read_csv('weather_now.csv', names=cols)
    data_now = data_now.dropna()
    day = preprocessing(data_now[['time', 'tempC', 'weatherDesc']].values)
    return day


def send_text1(message):
    now = datetime.datetime.now()
    predict = get_weather(now).T[2]
    vector1 = np.zeros(4)
    vector2 = np.zeros(4)
    for i in predict[8:12]:
        vector1[i]+=1
    vector1 =  vector1 / 4
    for i in predict[12:]:
        vector2[i]+=1
    vector2 =  vector2 / 4
    weather_matrix = np.load(open("data_processing/matrices/matrix1.npy","rb"))
    '''
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
        bot.send_message(message.chat.id, str(result))'''
    result1 = calculation1(now.month, vector1, weather_matrix)
    result2 = calculation1(now.month, vector2, weather_matrix)
    bot.send_message(message.chat.id, str(result1) + 'night')
    bot.send_message(message.chat.id, str(result2) + 'day')
    bot.send_message(message.chat.id, 'Для получения нового прогноза введите /start')


def comp(temp):
    result = np.zeros(5)
    for i in temp:
        if i < -5:
            result[0] += 1
        elif (i >= -5) and (i < -2):
            result[1] += 1
        elif (i >= -2) and (i <= 2):
            result[2] += 1
        elif (i > 2) and (i <= 5):
            result[3] += 1
        else:
            result[4] += 1
    return result / 4


def temp_diff(data):
    result = np.array([])
    night1 = data[:4]
    day1 = data[4:8]
    night2 = data[8:12]
    day2 = data[12:]
    t1 = night2.mean()
    t2 = day2.mean()
    res1 = comp(night2 - night1)
    res2 = comp(day2 - day1)
    return res1, res2, t1, t2


def send_text2(message):
    now = datetime.datetime.now()
    result_t1, result_t2, t1, t2 = temp_diff(get_weather(now).T[1])
    temp_matrix = np.load(open("data_processing/matrices/matrix2.npy","rb"))
    
    '''
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
    '''
    result1 = calculation2(now.month, result_t1, temp_matrix)
    result2 = calculation2(now.month, result_t2, temp_matrix)
    bot.send_message(message.chat.id, str(t1) + ' ' + str(result1) + '- night')
    bot.send_message(message.chat.id, str(t2) + ' ' + str(result2) + '- day')
    bot.send_message(message.chat.id, 'Для получения нового прогноза введите /start')


@bot.message_handler(content_types=['text'])
def type_predction(message):
    if message.text.lower() == 'общий прогноз':
        #bot.send_message(message.chat.id, 'Чтобы узнать погоду в Долгопрудном на завтра, мне нужно знать сегодняшнюю. Для ее описания выберете наиболее подходящий вариант',
        #                 reply_markup=keyboard1)
        send_text1(message)
    elif message.text.lower() == 'прогнозирование температуры':
        #bot.send_message(message.chat.id, 'Чтобы узнать погоду в Долгопрудном на завтра, мне нужно знать сегодняшнюю. Для ее описания выберете наиболее подходящий вариант',
        #                 reply_markup=keyboard2)
        send_text2(message)
    elif message.text in list1:
        send_text1(message)
    elif message.text in list2:
        send_text2(message)


bot.polling()
