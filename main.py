import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import dict
import functions as f

token = '5293678705:AAEMhxsad5TOEVBXSHga9J5Ijh42UrpNKVQ'
bot = telebot.TeleBot(token, threaded=False)


@bot.message_handler(commands=['start', 'help'])
def start_message(message):

    first_name = message.from_user.first_name
    print('Start', first_name)
    text = f'Привет, {first_name}!\nДобро пожаловать! Я бот-помошник! Напиши свои симптомы подробно в одном сообщении'
    chat_id = message.chat.id
    bot.send_message(chat_id=chat_id, text=text)


@bot.message_handler(content_types='text')
def send_message(message):
    msg = message.text
    first_name = message.from_user.first_name
    print('Text', first_name, msg)
    chat_id = message.chat.id
    if len(msg) < 20:
        bot.send_message(chat_id=chat_id, text='Напиши более подробно')
    else:
        bot.send_message(chat_id=chat_id, text='Обрабатываю данные. Пожалуйста, подожди...')

        m_lemmas = f.lemmatization(msg)

        predict_dict = {}

        for dis in dict.disease:
            match = f.match_percentage(dis['lemmas'], m_lemmas)
            if match > 0:
                predict_dict[f'{dis["name"]}'] = match
        if len(predict_dict) > 0:
            sorted_names = sorted(predict_dict, key=predict_dict.get, reverse=True)[:3]
            markup_inline = InlineKeyboardMarkup()
            text = 'Пораскинув ноликами и единичками, я могу сообщить, что вероятность болезни:'
            for sorted_name in sorted_names:
                markup_inline.add(InlineKeyboardButton(text=f'{sorted_name}', callback_data=f'{sorted_name}'))
                text += f'\n{sorted_name}: {predict_dict[sorted_name]}%'
            text += '\n\nКликни по кнопке, чтобы узнать подробнее о болезни'
            bot.send_message(chat_id=chat_id, text=text, reply_markup=markup_inline)
        else:
            bot.send_message(chat_id=chat_id, text='Анализ не выявил никаких совпадений с базой болезней')
        print('predict', predict_dict)


@bot.callback_query_handler(func=lambda call: True)
def answer_to_call(call):
    print('Callback:', call.data)
    callback = call.data
    chat_id = call.message.chat.id
    for dis in dict.disease:
        if dis['name'] == callback:
            bot.send_message(chat_id=chat_id, text=dis['description'])
            break



f.add_lemmas()
print('Бот запущен')
while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)
        print('Бот перезапущен')
