import datetime
import numpy as np
import telebot
import requests
import csv
import collections
import pandas as pd
from functools import cmp_to_key
from sklearn.externals import joblib


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

keyboard3 = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
keyboard3.row('ML', 'MarkovChain')


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id,
                     'Привет, я умею делать общий прогноз погоды и предсказывать температуру в городе Долгопрудном. Какой прогноз Вы бы хотели получить?',
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


def my_cmp(a, b):
    return b[0] - a[0]


def translation1(vector):
    maximum = max(vector)
    res1 = []
    res2 = []
    vector = vector / maximum
    support = [(vector[i], int(i)) for i in range(len(vector))]
    support = sorted(support, key=cmp_to_key(my_cmp))
    names = list1[:4]
    i = 0
    while i < len(vector):
        if support[i][0] > 0.8:
            res1.append(names[support[i][1]])
        elif support[i][0] > 0.5:
            res2.append(names[support[i][1]])
        i += 1
    return res1, res2


def translation2(vector):
    maximum = max(vector)
    res1 = []
    res2 = []
    vector = vector / maximum
    support = [(vector[i], int(i)) for i in range(len(vector))]
    support = sorted(support, key=cmp_to_key(my_cmp))
    names = list2[:5]
    i = 0
    if names[support[0][1]] == list2[0]:
        return (-5, 0)
    elif names[support[0][1]] == list2[1]:
        return (-5, -2)
    elif names[support[0][1]] == list2[2]:
        return (-2, 2)
    elif names[support[0][1]] == list2[3]:
        return (2, 5)
    elif names[support[0][1]] == list2[4]:
        return (5, 0)
    '''while i < len(vector):
        if support[i][0] > 0.9:
            res1.append(names[support[i][1]])
        elif support[i][0] > 0.5:
            res2.append(names[support[i][1]])
        i += 1
    #return res1, res2
    '''


def preprocessing(data):
    processing_data = data
    for i in processing_data:
        if i[2] in {'Thundery outbreaks possible', 'Moderate rain',
                    'Light drizzle', 'Light freezing rain', 'Moderate or heavy rain shower',
                    'Patchy rain possible', 'Light rain shower', 'Patchy light drizzle',
                    'Light rain', 'Moderate or heavy rain with thunder',
                    'Moderate rain at times', 'Heavy rain', 'Patchy light rain',
                    'Patchy light rain with thunder'}:
            i[2] = 2
        elif i[2] in {'Light snow', 'Patchy moderate snow', 'Heavy freezing drizzle',
                      'Moderate snow', 'Heavy snow', 'Light snow showers',
                      'Moderate or heavy sleet', 'Moderate or heavy snow showers',
                      'Light sleet', 'Light sleet showers', 'Patchy snow possible',
                      'Blizzard', 'Patchy heavy snow', 'Patchy light snow'}:
            i[2] = 3
        elif i[2] in {'Fog', 'Overcast', 'Freezing fog', 'Mist', 'Partly cloudy'}:
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


def names(str1, str2):
    name1 = ''
    name2 = ''
    i = 0
    while i < len(str1) - 1:
        name1 += str1[i].lower() + ', '
        i += 1
    name1 += str1[i].lower()
    i = 0
    if len(str2) >= 1:
        while i < len(str2) - 1:
            name2 += str2[i].lower() + ', '
            i += 1
        name2 += str2[i].lower()
    return name1, name2


def send_text1(message):
    now = datetime.datetime.now()
    predict = get_weather(now).T[2]
    vector1 = np.zeros(4)
    vector2 = np.zeros(4)
    for i in predict[8:12]:
        vector1[i] += 1
    vector1 = vector1 / 4
    for i in predict[12:]:
        vector2[i] += 1
    vector2 = vector2 / 4
    weather_matrix = np.load(open("data_processing/matrices/matrix1.npy", "rb"))
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
    night1, night2 = translation1(result1)
    day1, day2 = translation1(result2)
    name_n1, name_n2 = names(night1, night2)
    name_d1, name_d2 = names(day1, day2)
    if len(night2) > 0:
        bot.send_message(message.chat.id, 'Ночью будет ' + name_n1 + ', возможно ' + name_n2 + ".")
    else:
        bot.send_message(message.chat.id, 'Ночью будет ' + name_n1 + ".")
    if len(day2) > 0:
        bot.send_message(message.chat.id, 'Днем будет ' + name_d1 + ', возможно ' + name_d2 + ".")
    else:
        bot.send_message(message.chat.id, 'Днем будет ' + name_d1 + ".")
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
    temp_matrix = np.load(open("data_processing/matrices/matrix2.npy", "rb"))
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
    (night1, night2) = translation2(result1)
    (day1, day2) = translation2(result2)
    if night2 == 0:
        if night1 > 0:
            bot.send_message(message.chat.id, 'Наиболее вероятно, что ночью температура поднимется выше ' + str(t1 + night1) + ' градусов.')
        else:
            bot.send_message(message.chat.id, 'Наиболее вероятно, что ночью температура опустится ниже ' + str(t1 + night2) + ' градусов.')
    else:
        bot.send_message(message.chat.id, 'Наиболее вероятно, что ночью температура будет в пределах от ' + str(t1 + night1) + ' до ' + str(t1 + night2) + ' градусов.')
    if day2 == 0:
        if day1 > 0:
            bot.send_message(message.chat.id, 'Наиболее вероятно, что днем температура поднимется выше ' + str(t2 + day1) + ' градусов.')
        else:
            bot.send_message(message.chat.id, 'Наиболее вероятно, что днем температура опустится ниже ' + str(t2 + day1) + ' градусов.')
    else:
        bot.send_message(message.chat.id, 'Наиболее вероятно, что днем температура будет в пределах от ' + str(t2 + day1) + ' до ' + str(t2 + day2) + ' градусов.')
    bot.send_message(message.chat.id, 'Для получения нового прогноза введите /start')


def ML_predict(message):
    now = datetime.datetime.now()
    _joblib = joblib.load('method.pkl')
    res = round(float(_joblib.predict([[now.day, now.month, now.year]])), 1)
    bot.send_message(message.chat.id, 'Наиболее вероятно, что завтра температура будет около ' + str(res) + ' градусов.')
    bot.send_message(message.chat.id, 'Для получения нового прогноза введите /start')


@bot.message_handler(content_types=['text'])
def type_predction(message):
    if message.text.lower() == 'общий прогноз':
        # bot.send_message(message.chat.id, 'Чтобы узнать погоду в Долгопрудном на завтра, мне нужно знать сегодняшнюю. Для ее описания выберете наиболее подходящий вариант',
        #                 reply_markup=keyboard1)
        send_text1(message)
    elif message.text.lower() == 'прогнозирование температуры':
        bot.send_message(message.chat.id, 'Выберете способ предсказания:', reply_markup=keyboard3)
    elif message.text.lower() == 'ml':
        ML_predict(message)
    elif message.text.lower() == 'markovchain':
        send_text2(message)
    elif message.text in list1:
        send_text1(message)
    elif message.text in list2:
        send_text2(message)


bot.polling()
