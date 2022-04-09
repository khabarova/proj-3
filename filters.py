import telebot
from telebot import types
import sqlite3
from random import randint

# токен бота
bot = telebot.TeleBot('5211894904:AAFbuovu8W1VefPHBOffusDFwSppYqjB_0Q')
# count_button, для того чтобы обрабатывать 1 нажатие кнопки
count_button = 0
# случайное id  для будущего
rand_id1 = randint(1, 10)
# случайное id для прошлого
rand_id2 = randint(1, 10)

con = sqlite3.connect("base3.db")
cur = con.cursor()

name1 = (cur.execute(f'SELECT name FROM user WHERE id={rand_id1}').fetchall()[0][0])
luck1 = (cur.execute(f'SELECT luck FROM user WHERE id={rand_id1}').fetchall()[0][0])
authority1 = (cur.execute(f'SELECT authority FROM user WHERE id={rand_id1}').fetchall()[0][0])
health1 = (cur.execute(f'SELECT health FROM user WHERE id={rand_id1}').fetchall()[0][0])

name2 = (cur.execute(f'SELECT name FROM user WHERE id={rand_id2}').fetchall()[0][0])
luck2 = (cur.execute(f'SELECT luck FROM user WHERE id={rand_id2}').fetchall()[0][0])
authority2 = (cur.execute(f'SELECT authority FROM user WHERE id={rand_id2}').fetchall()[0][0])
health2 = (cur.execute(f'SELECT health FROM user WHERE id={rand_id2}').fetchall()[0][0])


# функция для вступления
@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == '/start':
        global count_button
        bot.send_message(message.from_user.id, "Приветствую! Вы попали в квест-лабиринт. "
                                               "Используя бота, вы можете погрузиться в "
                                               "мир удивительных историй и загадок."
                                               " От каждого вашего выбора, зависит судьба персонажа и исход игры.")
        # клавиатура
        keyboard = types.InlineKeyboardMarkup()
        # кнопка «Да»
        key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')
        # добавление кнопки в клавиатуру
        keyboard.add(key_yes)
        # кнопка «Нет»
        key_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
        keyboard.add(key_no)
        question = "Хотите начать?"
        bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)
    if message.text == '/ready' and count_button == 1:
        ask(message)
    if message.text == '/help':
        bot.send_message(message.from_user.id, 'Функция помощник. Я не могу обработать ваши сообщения. '
                                               'Пожалуйста нажимайте только на те кнопки,'
                                               ' которые вам выводит приложение')
    if message.text == '/school' and count_button == 2:
        first_ask_future(message)
    if message.text != '/help' and message.text != '/start' and message.text != '/ready' and message.text != '/school' \
            or (message.text == '/ready' and count_button != 1) or (message.text == '/school' and count_button != 2):
        bot.send_message(message.from_user.id, 'Я вас не понимаю( Напишите /help')


# обработка выбора пользователя
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    # call.data это callback_data, которую мы указали при объявлении кнопки
    global count_button
    global rand_id
    # начало
    if call.data == "yes" and count_button == 0:
        count_button += 1
        bot.send_message(call.message.chat.id, 'Поехали',
                         reply_markup=types.ReplyKeyboardRemove(), parse_mode='Markdown')
        bot.send_message(call.message.chat.id, 'О! Вижу вы решили попытаться пройти квест. Удачи. Для начала выберите'
                                               'время действий. Напишите /ready.')

    # завершение
    if call.data == "no" and count_button == 0:
        count_button += 1
        bot.send_message(call.message.chat.id, 'Пока-пока! Заглядывайте к нам еще)',
                         reply_markup=types.ReplyKeyboardRemove(), parse_mode='Markdown')

    # будущее
    if call.data == "future" and count_button == 1:
        # характеристики для будущего
        count_button += 1
        bot.send_message(call.message.chat.id, '''3100 год от Рождества Христово. Галактика Андромеды.
Планета «NL-31» - ближайшая планета с климатом пригодным для жизни. Человеческая раса перебралась
жить на эту планету из-за разрушения ядра планеты Земля. Время на планете «NL-31» течет в 2 раза
медленнее земного, а вместо Солнца – звезда «Мабу».''')
        bot.send_message(call.message.chat.id, f'''Сегодня день Вашего рождения.
Ваше имя - {name1}, 
Ваша удача - {luck1}, 
Ваш авторитет- {authority1}, 
Ваше здоровье - {health1}.''')
        bot.send_message(call.message.chat.id, '''Первые 7 лет жизни были не особо захватывающими,
Вы обретали навыки ходьбы, общения, чтения, счета. В 7 лет Вы пошли в школу. Напише /school. ''')

    # прошлое
    if call.data == "past" and count_button == 1:
        # характеристики для прошлого
        count_button += 1
        bot.send_message(call.message.chat.id, '''Лучи палящего солнца неприятно светят вам в глаза.
Шум голосов становится все громче. Вы жмуритесь сильнее, в попытках вернуться в сладкое царство морфея.
Но тщетно. Злобная старуха Сафо - хозяйка гостиницы, под чьими окнами вы уснули- окатывает вас ледяной водой. 
Не успев, прийти в себя, вы сталкиваетесь с возмущением хозяйки. "А ка зараза ко мне повадилась!
Проку от тебя ноль. Запомни уже, я тебя давно уволила. Не смей, больше сюда приходить, только портишь вид
моему заведению!!! В следующий раз вылью кипящую смолу!!!" - прокричала вам карга Сафо. Мда...
Судьба у вас не завидная. Хотя кому щас легко? На дворе 675 г. до н.э., Греция, остров Крит. Сильная засуха,
голод, нехватка работы из-за большого количество захваченных рабов. Конечно же, им то платить не надо: 
дал кувшин воды, да яблок штук 7 и ходят себе счастливые.... Ну да ладно, начался новый день, 
а значит надо снова отправляться на поиски новый работы!.''')
        # из бд выводим имя и остальные параметры, соответствующие id
        bot.send_message(call.message.chat.id, f''' Ваша краткая биография.
Имя - {name2}, 
Уровень удачи - {luck2}, 
Авторитет- {authority2}, 
Уровень здоровья - {health2}.''')

    # поздороваться с Егором
    if call.data == "hi" and count_button == 2:
        count_button += 1
        # надо как-то сделать + авторитет
        bot.send_message(call.message.chat.id, '''С Егором вы стали сидеть за одной партой и довольно сильно сдружились.''')
        bot.send_message(call.message.chat.id, '''Так из года в год (все 10 лет) проходит каждый Ваш день: 
школа, домашнее задание, сон.''')

    # промолчать
    if call.data == "molchat" and count_button == 2:
        count_button += 1
        # надо как-то сделать - авторитет
        bot.send_message(call.message.chat.id, '''Егор обиделся и всем сказал, что с Вами нельзя дружить. 
Теперь вы сидите в одиночестве.''')
        bot.send_message(call.message.chat.id, '''Так из года в год (все 10 лет) проходит каждый Ваш день:
школа, домашнее задание, сон.''')
        bot.send_message(call.message.chat.id, '''3 апреля 3116 года. Этот день вы запомните на всю жизнь.
Тогда учитель попросил Вас принести из соседней аудитории несколько пар микроскопов для лабораторной работы. 
Вы зашли в лаборантскую и увидели на полу человека с пробитой головой. Рана была свежая, и 10 минут не было. Рядом лежал микроскоп весь в крови.
Вы взяли его и тут же поняли какую ошибку совершили...''')
        # bot.send_message(call.message.chat.id, '''///''')


def ask(message):
    keyboard = types.InlineKeyboardMarkup()
    # кнопка «Будущее»
    key_future = types.InlineKeyboardButton(text='Будущее!', callback_data='future')
    # добавление кнопки в клавиатуру
    keyboard.add(key_future)
    # кнопка «Прошлое»
    key_ancient = types.InlineKeyboardButton(text='Прошлое!', callback_data='past')
    keyboard.add(key_ancient)
    question = "Сетинг квеста:"
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)


def first_ask_future(message):
    keyboard = types.InlineKeyboardMarkup()
    # кнопка «Будущее»
    key_future = types.InlineKeyboardButton(text=f'"Привет, я {name1}"', callback_data='hi')
    # добавление кнопки в клавиатуру
    keyboard.add(key_future)
    # кнопка «Прошлое»
    key_ancient = types.InlineKeyboardButton(text='промолчать*', callback_data='molchat')
    keyboard.add(key_ancient)
    question = "Одноклассник: Привет, я Егор, как тебя зовут?"
    bot.send_message(message.chat.id, text=question, reply_markup=keyboard)


bot.polling()
