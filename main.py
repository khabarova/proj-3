import telebot
from telebot import types

bot = telebot.TeleBot('5211894904:AAFbuovu8W1VefPHBOffusDFwSppYqjB_0Q')


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "/start":
        bot.register_next_step_handler(message, quest)
    else:
        bot.send_message(message.from_user.id, "Напиши /start.")


def quest(message):
    keyboard = types.InlineKeyboardMarkup()
    key_yes = types.InlineKeyboardButton(text='Прошлое', callback_data='1')
    keyboard.add(key_yes)
    key_no = types.InlineKeyboardButton(text='Будущее', callback_data='2')
    keyboard.add(key_no)
    question = 'Вас пиветствует QuestBot, в какое время отправимся? Выбирай с умом'
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "1":
        bot.send_message(call.message.chat.id, 'Отправляемся в прошлое')
    elif call.data == "2":
        bot.send_message(call.message.chat.id, 'Отправляемся в будущее')


bot.polling(none_stop=True, interval=0)
