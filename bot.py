import telebot
import numpy as np
import datetime

# t.me/markov_weather_bot
# api token: 1281314124:AAH9KihH1H3ziKdmKFWv9QBU0XXpLKrFk1g
# vpn_connect: windscribe connect
# windscribe --help

bot = telebot.TeleBot('1281314124:AAH9KihH1H3ziKdmKFWv9QBU0XXpLKrFk1g')

keyboard1 = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
keyboard1.row('Ясно', 'Облачно', 'Дождь')
keyboard1.row('Снег', 'Переменная обачность')
keyboard1.row('Ясно, временами дождь', 'Ясно, временами снег')
keyboard1.row('Облачно, дождь', 'Облачно, снег', 'Мокрый снег, дождь')                

M1 = np.array([[0.76530612, 0.01020408, 0.05102041, 0.17346939],
                [0.        , 0.38983051, 0.22033898, 0.38983051],
                [0.00897666, 0.02154399, 0.70556553, 0.26391382],
                [0.01927195, 0.02462527, 0.15631692, 0.79978587]])

M2 = np.array([[0.59210526, 0.10526316, 0.03947368, 0.26315789],
                [0.04347826, 0.53913043, 0.16521739, 0.25217391],
                [0.01515152, 0.0479798 , 0.68939394, 0.24747475],
                [0.02699055, 0.03508772, 0.13765182, 0.80026991]])

M3 = np.array(([[0.75824176, 0.02197802, 0.08241758, 0.13736264],
                [0.1       , 0.61111111, 0.2       , 0.08888889],
                [0.03519669, 0.04140787, 0.7826087 , 0.14078675],
                [0.04009434, 0.0259434 , 0.16981132, 0.76415094]]))

M4 = np.array(([[0.78947368, 0.01052632, 0.16315789, 0.03684211],
                [0.0952381 , 0.46031746, 0.42857143, 0.01587302],
                [0.04836193, 0.04524181, 0.85647426, 0.049922  ],
                [0.03409091, 0.02272727, 0.39772727, 0.54545455]]))

M5 = np.array([[0.79234973, 0.00546448, 0.20218579, 0.        ],
                [0.03448276, 0.31034483, 0.65517241, 0.        ],
                [0.06595365, 0.03386809, 0.89304813, 0.00713012],
                [0.        , 0.        , 0.8       , 0.2       ]])

M6 = np.array([[0.75862069, 0.01149425, 0.22988506, 0.        ],
                [0.06666667, 0.46666667, 0.46666667, 0.        ],
                [0.03610108, 0.01263538, 0.95126354, 0.        ],
                [0.25      , 0.25      , 0.25      , 0.25      ]])

M7 = np.array([[0.74      , 0.04      , 0.22      , 0.        ],
                [0.075     , 0.475     , 0.45      , 0.        ],
                [0.04408818, 0.03406814, 0.92184369, 0.        ],
                [0.25      , 0.25      , 0.25      , 0.25      ]])

M8 = np.array([[0.64035088, 0.07017544, 0.28947368, 0.        ],
                [0.06024096, 0.62650602, 0.31325301, 0.        ],
                [0.07072692, 0.04518664, 0.88408644, 0.        ],
                [0.25      , 0.25      , 0.25      , 0.25      ]])

M9 = np.array(([[0.65384615, 0.11538462, 0.23076923, 0.        ],
                [0.23404255, 0.38297872, 0.38297872, 0.        ],
                [0.03888025, 0.02643857, 0.93312597, 0.00155521],
                [0.        , 0.        , 1.        , 0.        ]]))

M10 = np.array([[0.72151899, 0.07594937, 0.18987342, 0.01265823],
                [0.05084746, 0.42372881, 0.45762712, 0.06779661],
                [0.02460203, 0.03328509, 0.88712012, 0.05499276],
                [0.01449275, 0.03623188, 0.26086957, 0.6884058 ]])

M11 = np.array([[0.72916667, 0.13541667, 0.0625    , 0.07291667],
                [0.03626943, 0.70466321, 0.1865285 , 0.07253886],
                [0.01671733, 0.04559271, 0.83890578, 0.09878419],
                [0.02      , 0.04285714, 0.18285714, 0.75428571]])

M12 = np.array([[0.58974359, 0.02564103, 0.12820513, 0.25641026],
                [0.        , 0.51145038, 0.23664122, 0.2519084 ],
                [0.00633914, 0.05388273, 0.74167987, 0.19809826],
                [0.01503759, 0.03634085, 0.15914787, 0.78947368]])


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 
                        'Привет, чтобы узнать погоду на завтра, мне нужно знать сегодняшнюю' )
    bot.send_message(message.chat.id, 
                        'Для ее описание выберите наиболее подходящий варинат', reply_markup=keyboard1)

def calculation(now, vector):
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
        

@bot.message_handler(content_types=['text'])
def send_text(message):
    now = datetime.datetime.now()
    if message.text.lower() == 'ясно':
        vector = np.array([1, 0, 0, 0])
        result = calculation(now.month, vector)
        bot.send_message(message.chat.id, str(result))
    elif message.text.lower() == 'облачно':
        vector = np.array([0, 1, 0, 0])
        result = calculation(now.month, vector)
        bot.send_message(message.chat.id, str(result))
    elif message.text.lower() == 'дождь':
        vector = np.array([0, 0, 1, 0])
        result = calculation(now.month, vector)
        bot.send_message(message.chat.id, str(result))
    elif message.text.lower() == 'снег':
        vector = np.array([0, 0, 0, 1])
        result = calculation(now.month, vector)
        bot.send_message(message.chat.id, str(result))
    elif message.text.lower() == 'переменная обачность':
        vector = np.array([0.5, 0.5, 0, 0])
        result = calculation(now.month, vector)
        bot.send_message(message.chat.id, str(result))
    elif message.text.lower() == 'ясно, временами дождь':
        vector = np.array([0.5, 0.25, 0.25, 0])
        result = calculation(now.month, vector)
        bot.send_message(message.chat.id, str(result))
    elif message.text.lower() == 'ясно, временами снег':
        vector = np.array([0.5, 0.1, 0, 0.4])
        result = calculation(now.month, vector)
        bot.send_message(message.chat.id, str(result))
    elif message.text.lower() == 'облачно, дождь':
        vector = np.array([0, 0.5, 0.5, 0])
        result = calculation(now.month, vector)
        bot.send_message(message.chat.id, str(result))
    elif message.text.lower() == 'облачно, снег':
        vector = np.array([0, 0.5, 0, 0.5])
        result = calculation(now.month, vector)
        bot.send_message(message.chat.id, str(result))
    elif message.text.lower() == 'мокрый снег, дождь':
        vector = np.array([0, 0.2, 0.4, 0.4])
        result = calculation(now.month, vector)
        bot.send_message(message.chat.id, str(result))
    bot.send_message(message.chat.id, 'Для получения нового прогноза введите /start')


bot.polling()