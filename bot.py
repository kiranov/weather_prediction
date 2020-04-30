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


M1 = np.array([[0.76530612, 0.01020408, 0.05102041, 0.17346939],
               [0., 0.38983051, 0.22033898, 0.38983051],
               [0.00897666, 0.02154399, 0.70556553, 0.26391382],
               [0.01927195, 0.02462527, 0.15631692, 0.79978587]])

M2 = np.array([[0.59210526, 0.10526316, 0.03947368, 0.26315789],
               [0.04347826, 0.53913043, 0.16521739, 0.25217391],
               [0.01515152, 0.0479798, 0.68939394, 0.24747475],
               [0.02699055, 0.03508772, 0.13765182, 0.80026991]])

M3 = np.array(([[0.75824176, 0.02197802, 0.08241758, 0.13736264],
                [0.1, 0.61111111, 0.2, 0.08888889],
                [0.03519669, 0.04140787, 0.7826087, 0.14078675],
                [0.04009434, 0.0259434, 0.16981132, 0.76415094]]))

M4 = np.array(([[0.78947368, 0.01052632, 0.16315789, 0.03684211],
                [0.0952381, 0.46031746, 0.42857143, 0.01587302],
                [0.04836193, 0.04524181, 0.85647426, 0.049922],
                [0.03409091, 0.02272727, 0.39772727, 0.54545455]]))

M5 = np.array([[0.79234973, 0.00546448, 0.20218579, 0.],
               [0.03448276, 0.31034483, 0.65517241, 0.],
               [0.06595365, 0.03386809, 0.89304813, 0.00713012],
               [0., 0., 0.8, 0.2]])

M6 = np.array([[0.75862069, 0.01149425, 0.22988506, 0.],
               [0.06666667, 0.46666667, 0.46666667, 0.],
               [0.03610108, 0.01263538, 0.95126354, 0.],
               [0.25, 0.25, 0.25, 0.25]])

M7 = np.array([[0.74, 0.04, 0.22, 0.],
               [0.075, 0.475, 0.45, 0.],
               [0.04408818, 0.03406814, 0.92184369, 0.],
               [0.25, 0.25, 0.25, 0.25]])

M8 = np.array([[0.64035088, 0.07017544, 0.28947368, 0.],
               [0.06024096, 0.62650602, 0.31325301, 0.],
               [0.07072692, 0.04518664, 0.88408644, 0.],
               [0.25, 0.25, 0.25, 0.25]])

M9 = np.array(([[0.65384615, 0.11538462, 0.23076923, 0.],
                [0.23404255, 0.38297872, 0.38297872, 0.],
                [0.03888025, 0.02643857, 0.93312597, 0.00155521],
                [0., 0., 1., 0.]]))

M10 = np.array([[0.72151899, 0.07594937, 0.18987342, 0.01265823],
                [0.05084746, 0.42372881, 0.45762712, 0.06779661],
                [0.02460203, 0.03328509, 0.88712012, 0.05499276],
                [0.01449275, 0.03623188, 0.26086957, 0.6884058]])

M11 = np.array([[0.72916667, 0.13541667, 0.0625, 0.07291667],
                [0.03626943, 0.70466321, 0.1865285, 0.07253886],
                [0.01671733, 0.04559271, 0.83890578, 0.09878419],
                [0.02, 0.04285714, 0.18285714, 0.75428571]])

M12 = np.array([[0.58974359, 0.02564103, 0.12820513, 0.25641026],
                [0., 0.51145038, 0.23664122, 0.2519084],
                [0.00633914, 0.05388273, 0.74167987, 0.19809826],
                [0.01503759, 0.03634085, 0.15914787, 0.78947368]])

T1 = np.array([[0.15, 0.1, 0.35, 0.2, 0.2],
               [0.04819277, 0.10843373, 0.53012048, 0.19277108, 0.12048193],
               [0.02531646, 0.17721519, 0.67721519, 0.10126582, 0.01898734],
               [0.02985075, 0.19402985, 0.59701493, 0.14925373, 0.02985075],
               [0.125, 0.125, 0.45833333, 0.20833333, 0.08333333]])

T2 = np.array([[0., 0.09090909, 0.33333333, 0.18181818, 0.39393939],
               [0.07462687, 0.08955224, 0.40298507, 0.29850746, 0.13432836],
               [0.0625, 0.15625, 0.59375, 0.16517857, 0.02232143],
               [0.11842105, 0.22368421, 0.52631579, 0.11842105, 0.01315789],
               [0.17857143, 0.21428571, 0.5, 0.10714286, 0.]])

T3 = np.array([[0.04444444, 0.08888889, 0.26666667, 0.22222222, 0.37777778],
               [0.06849315, 0.08219178, 0.43835616, 0.26027397, 0.15068493],
               [0.07734807, 0.19889503, 0.53038674, 0.14364641, 0.04972376],
               [0.19354839, 0.30645161, 0.41935484, 0.03225806, 0.0483871],
               [0.27906977, 0.18604651, 0.37209302, 0.11627907, 0.04651163]])

T4 = np.array([[0.04918033, 0.08196721, 0.16393443, 0.27868852, 0.42622951],
               [0.04166667, 0.125, 0.375, 0.23611111, 0.22222222],
               [0.08403361, 0.13445378, 0.4789916, 0.23529412, 0.06722689],
               [0.3, 0.35714286, 0.25714286, 0.04285714, 0.04285714],
               [0.43636364, 0.30909091, 0.14545455, 0.09090909, 0.01818182]])

T5 = np.array([[0.05882353, 0.07843137, 0.29411765, 0.2745098, 0.29411765],
               [0.01851852, 0.05555556, 0.42592593, 0.22222222, 0.27777778],
               [0.07079646, 0.21238938, 0.40707965, 0.18584071, 0.12389381],
               [0.28070175, 0.24561404, 0.28070175, 0.10526316, 0.0877193],
               [0.44230769, 0.17307692, 0.26923077, 0.07692308, 0.03846154]])

T6 = np.array([[0., 0.11428571, 0.34285714, 0.14285714, 0.4],
               [0.05263158, 0.0877193, 0.36842105, 0.31578947, 0.1754386],
               [0.11494253, 0.29885057, 0.31034483, 0.18390805, 0.09195402],
               [0.1875, 0.25, 0.41666667, 0.10416667, 0.04166667],
               [0.36111111, 0.27777778, 0.19444444, 0.11111111, 0.05555556]])

T7 = np.array([[0.10810811, 0.05405405, 0.32432432, 0.16216216, 0.35135135],
               [0., 0.05660377, 0.35849057, 0.26415094, 0.32075472],
               [0.04901961, 0.19607843, 0.41176471, 0.25490196, 0.08823529],
               [0.10416667, 0.375, 0.5, 0., 0.02083333],
               [0.54761905, 0.23809524, 0.14285714, 0.04761905, 0.02380952]])

T8 = np.array([[0., 0.04444444, 0.31111111, 0.17777778, 0.46666667],
               [0.01538462, 0.07692308, 0.38461538, 0.35384615, 0.16923077],
               [0.0990099, 0.23762376, 0.43564356, 0.13861386, 0.08910891],
               [0.14893617, 0.5106383, 0.23404255, 0.0212766, 0.08510638],
               [0.58695652, 0.19565217, 0.17391304, 0.02173913, 0.02173913]])

T9 = np.array([[0., 0.08, 0.48, 0.24, 0.2],
               [0.03225806, 0.12903226, 0.46774194, 0.30645161, 0.06451613],
               [0.0308642, 0.16049383, 0.59876543, 0.14814815, 0.0617284],
               [0.07407407, 0.40740741, 0.40740741, 0.05555556, 0.05555556],
               [0.63636364, 0.18181818, 0.13636364, 0.04545455, 0.]])

T10 = np.array([[0.05555556, 0., 0.66666667, 0.16666667, 0.11111111],
                [0.05263158, 0.12280702, 0.54385965, 0.21052632, 0.07017544],
                [0.03301887, 0.16509434, 0.63207547, 0.12264151, 0.04716981],
                [0., 0.26, 0.54, 0.14, 0.06],
                [0.36842105, 0.10526316, 0.47368421, 0.05263158, 0.]])

T11 = np.array([[0., 0.17647059, 0.52941176, 0.23529412, 0.05882353],
                [0.07407407, 0.09259259, 0.48148148, 0.16666667, 0.18518519],
                [0.03214286, 0.13571429, 0.73571429, 0.08571429, 0.01071429],
                [0.06666667, 0.11111111, 0.6, 0.15555556, 0.06666667],
                [0.05882353, 0.17647059, 0.70588235, 0.05882353, 0.]])

T12 = np.array([[0., 0.15384615, 0.30769231, 0.23076923, 0.30769231],
                [0.03125, 0.109375, 0.6875, 0.140625, 0.03125],
                [0.02654867, 0.12979351, 0.73746313, 0.08849558, 0.01769912],
                [0.03030303, 0.16666667, 0.53030303, 0.25757576, 0.01515152],
                [0., 0., 0.5, 0.42857143, 0.07142857]])


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id,
                     'Привет, я умею делать общий прогноз погоды и предсказывать температуру. Какой прогноз Вы бы хотели получить?',
                     reply_markup=keyboard0)


def calculation1(now, vector):
    month = now
    if month == 1:
        result = vector @ M1
    elif month == 2:
        result = vector @ M2
    elif month == 3:
        result = vector @ M3
    elif month == 4:
        result = vector @ M4
    elif month == 5:
        result = vector @ M5
    elif month == 6:
        result = vector @ M6
    elif month == 7:
        result = vector @ M7
    elif month == 8:
        result = vector @ M8
    elif month == 9:
        result = vector @ M9
    elif month == 10:
        result = vector @ M10
    elif month == 11:
        result = vector @ M11
    elif month == 12:
        result = vector @ M12
    return result


def calculation2(now, vector):
    month = now
    if month == 1:
        result = vector @ T1
    elif month == 2:
        result = vector @ T2
    elif month == 3:
        result = vector @ T3
    elif month == 4:
        result = vector @ T4
    elif month == 5:
        result = vector @ T5
    elif month == 6:
        result = vector @ T6
    elif month == 7:
        result = vector @ T7
    elif month == 8:
        result = vector @ T8
    elif month == 9:
        result = vector @ T9
    elif month == 10:
        result = vector @ T10
    elif month == 11:
        result = vector @ T11
    elif month == 12:
        result = vector @ T12
    return result


def send_text1(message):
    now = datetime.datetime.now()
    if message.text.lower() == 'ясно':
        vector = np.array([1, 0, 0, 0])
        result = calculation1(now.month, vector)
        bot.send_message(message.chat.id, str(result))
    elif message.text.lower() == 'облачно':
        vector = np.array([0, 1, 0, 0])
        result = calculation1(now.month, vector)
        bot.send_message(message.chat.id, str(result))
    elif message.text.lower() == 'дождь':
        vector = np.array([0, 0, 1, 0])
        result = calculation1(now.month, vector)
        bot.send_message(message.chat.id, str(result))
    elif message.text.lower() == 'снег':
        vector = np.array([0, 0, 0, 1])
        result = calculation1(now.month, vector)
        bot.send_message(message.chat.id, str(result))
    elif message.text.lower() == 'переменная обачность':
        vector = np.array([0.5, 0.5, 0, 0])
        result = calculation1(now.month, vector)
        bot.send_message(message.chat.id, str(result))
    elif message.text.lower() == 'ясно, временами дождь':
        vector = np.array([0.5, 0.25, 0.25, 0])
        result = calculation1(now.month, vector)
        bot.send_message(message.chat.id, str(result))
    elif message.text.lower() == 'ясно, временами снег':
        vector = np.array([0.5, 0.1, 0, 0.4])
        result = calculation1(now.month, vector)
        bot.send_message(message.chat.id, str(result))
    elif message.text.lower() == 'облачно, дождь':
        vector = np.array([0, 0.5, 0.5, 0])
        result = calculation1(now.month, vector)
        bot.send_message(message.chat.id, str(result))
    elif message.text.lower() == 'облачно, снег':
        vector = np.array([0, 0.5, 0, 0.5])
        result = calculation1(now.month, vector)
        bot.send_message(message.chat.id, str(result))
    elif message.text.lower() == 'мокрый снег, дождь':
        vector = np.array([0, 0.2, 0.4, 0.4])
        result = calculation1(now.month, vector)
        bot.send_message(message.chat.id, str(result))
    bot.send_message(message.chat.id, 'Для получения нового прогноза введите /start')


def send_text2(message):
    now = datetime.datetime.now()
    if message.text.lower() == '<-5':
        vector = np.array([1, 0, 0, 0, 0])
        result = calculation2(now.month, vector)
        bot.send_message(message.chat.id, str(result))
    elif message.text.lower() == '[-5; -2)':
        vector = np.array([0, 1, 0, 0, 0])
        result = calculation2(now.month, vector)
        bot.send_message(message.chat.id, str(result))
    elif message.text.lower() == '[-2; 2]':
        vector = np.array([0, 0, 1, 0, 0])
        result = calculation2(now.month, vector)
        bot.send_message(message.chat.id, str(result))
    elif message.text.lower() == '(2; 5]':
        vector = np.array([0, 0, 0, 1, 0])
        result = calculation2(now.month, vector)
        bot.send_message(message.chat.id, str(result))
    elif message.text.lower() == '>5':
        vector = np.array([0, 0, 0, 0, 1])
        result = calculation2(now.month, vector)
        bot.send_message(message.chat.id, str(result))
    bot.send_message(message.chat.id, 'Для получения нового прогноза введите /start')


@bot.message_handler(content_types=['text'])
def type_predction(message):
    if message.text.lower() == 'общий прогноз':
        bot.send_message(message.chat.id, 'Чтобы узнать погоду в Долгопрудном на завтра, мне нужно знать сегодняшнюю. Для ее описание выберете наиболее подходящий варинат',
                         reply_markup=keyboard1)
    elif message.text.lower() == 'прогнозирование температуры':
        bot.send_message(message.chat.id, 'Чтобы узнать погоду в Долгопрудном на завтра, мне нужно знать сегодняшнюю. Для ее описание выберете наиболее подходящий варинат',
                         reply_markup=keyboard2)
    elif message.text in list1:
        send_text1(message)
    elif message.text in list2:
        send_text2(message)


bot.polling()
