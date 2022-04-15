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

weapon = 0


# функция для вступления
@bot.message_handler(content_types=['text'])
def start(message):
    global count_button
    if message.text == '/start':
        count_button = 0
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

    if message.text == '/help':
        bot.send_message(message.from_user.id, 'Функция помощник. Я не могу обработать ваши сообщения. '
                                               'Пожалуйста нажимайте только на те кнопки,'
                                               'которые вам выводит приложение')

    if message.text == '/futCard':
        global luck1
        global authority1
        global health1
        bot.send_message(message.from_user.id, f'''Ваша удача - {luck1}, 
Ваш авторитет- {authority1}, 
Ваше здоровье - {health1}.''')

    if message.text == '/ready' and count_button == 1:
        ask(message)

    if message.text == '/school' and count_button == 2:
        first_ask_future(message)

    if message.text == '/protest' and count_button == 3:
        protest_ask_future(message)

        # ПРОШЛОЕ эпизод с попугаем
    if message.text == '/save' and count_button == 2:
        last_friend_parrot(message)

    # ПРОШЛОЕ эпизод с кораблем
    if message.text == '/continue' and count_button == 3:
        last_korabl(message)

    if message.text != '/help' and message.text != '/start' and message.text != '/futCard' and message.text != '/ready' and message.text != '/school' \
            and message.text != '/protest' and message.text != '/save' and message.text != '/continue'\
            or (message.text == '/ready' and count_button != 1)\
            or (message.text == '/school' and count_button != 2) \
            or (message.text == '/protest' and count_button != 3)\
            or (message.text == '/save' and count_button != 2) \
            or (message.text == '/continue' and count_button != 3):
        bot.send_message(message.from_user.id, 'Я вас не понимаю( Напишите /help')


# обработка выбора пользователя
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    # call.data это callback_data, которую мы указали при объявлении кнопки
    global count_button
    global health1
    global authority1
    global luck1
    global luck2
    global health2
    global authority2
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


# БУДУЩЕЕ
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
        bot.send_message(call.message.chat.id, '''Чтобы в дальнейшем смотреть свои статусы пишите /futCard''')
        bot.send_message(call.message.chat.id, '''Первые 7 лет жизни были не особо захватывающими,
Вы обретали навыки ходьбы, общения, чтения, счета. В 7 лет Вы пошли в школу. Напишите /school. ''')

    # поздороваться с Кевином
    if call.data == "hi" and count_button == 2:
        count_button += 1
        # повышение авторитета
        authority1 += 1
        bot.send_message(call.message.chat.id, ''' + АВТОРИТЕТ
С Кевином вы стали сидеть за одной партой и довольно сильно сдружились.''')
        bot.send_message(call.message.chat.id, '''Так из года в год (все 10 лет) проходит каждый Ваш день:
школа, домашнее задание, сон.''')
        bot.send_message(call.message.chat.id, '''3 апреля 3116 года. Этот день вы запомните на всю жизнь.
Тогда учитель попросил Вас принести из другой аудитории несколько пар микроскопов для лабораторной работы и дал Вам ключ. 
Вы открыли лаборантскую и увидели на полу человека с пробитой головой. Рана была свежая, и 10 минут не было. Рядом лежал 
микроскоп весь в крови. Вы взяли его и тут же поняли какую ошибку совершили...''')
        bot.send_message(call.message.chat.id, '''Вот вбегают учителя..
Полиция..
Вот вы сидите на допросе..''')
        bot.send_message(call.message.chat.id, '''Вот как все было:
- Я зашел в лаборантскую и увидел труп.
- Вы видели кого-то выходящего?
- Нет.
- А дверь была закрыта, когда Вы заходили?
- Да, на ключ.
- Напомните мне для чего вы туда пошли?
- Мой учитель химии, попросил  меня сходить за микроскопами для лабораторной работы.
- В зал суда приглашается Фрэнсис Фишер.''')
        bot.send_message(call.message.chat.id, '''Учитель сказал, что правда отдал ключ от аудитории и отправил за микроскопами, 
однако ключ от лаборантской был только у Галлагера. Преподаватель отрицал свое нахождение в лаборантской в тот день, 
также по его словам в тот кабинет в тот день заходили лишь Вы.''')
        bot.send_message(call.message.chat.id, '''Суд выносит Вам приговор - 60 суток в исправительной колонии для несовершеннолетних
до полного расскрытия дела, которым будет заниматься детектив - Джордж Пуаро. 
Если согласны или не согласны с приговором напишите /protest''')

    # промолчать
    if call.data == "molchat" and count_button == 2:
        count_button += 1
        # понижение авторитета
        authority1 -= 1
        bot.send_message(call.message.chat.id, ''' - АВТОРИТЕТ
Кевин обиделся и всем сказал, что с Вами нельзя дружить. 
Теперь вы сидите в одиночестве.''')
        bot.send_message(call.message.chat.id, '''Так из года в год (все 10 лет) проходит каждый Ваш день:
школа, домашнее задание, сон.''')
        bot.send_message(call.message.chat.id, '''3 апреля 3116 года. Этот день вы запомните на всю жизнь.
Тогда учитель попросил Вас принести из другой аудитории несколько пар микроскопов для лабораторной работы и дал Вам ключ. 
Вы открыли лаборантскую и увидели на полу человека с пробитой головой. Рана была свежая, и 10 минут не было. Рядом лежал 
микроскоп весь в крови. Вы взяли его и тут же поняли какую ошибку совершили...''')
        bot.send_message(call.message.chat.id, '''Вот вбегают учителя..
Полиция..
Вот вы сидите на допросе..''')
        bot.send_message(call.message.chat.id, '''Вот как все было:
- Я зашел в лаборантскую и увидел труп.
- Вы видели кого-то выходящего?
- Нет.
- А дверь была закрыта, когда Вы заходили?
- Да, на ключ.
- Напомните мне для чего вы туда пошли?
- Мой учитель химии, попросил  меня сходить за микроскопами для лабораторной работы.
- В зал суда приглашается Фрэнк Галлагер.''')
        bot.send_message(call.message.chat.id, '''Учитель сказал, что правда отдал ключ от аудитории и отправил за микроскопами, 
однако ключ от лаборантской был только у Галлагера. Преподаватель отрицал свое нахождение в лаборантской в тот день, 
также по его словам в тот кабинет в тот день заходили лишь Вы.''')
        bot.send_message(call.message.chat.id, '''Суд выносит Вам приговор - 60 суток в исправительной колонии для несовершеннолетних
до полного расскрытия дела, которым будет заниматься детектив - Джордж Пуаро. 
Если согласны или не согласны с приговором напишите /protest''')

    if call.data == "ploh" and count_button == 3:
        count_button += 1
        bot.send_message(call.message.chat.id, '''Вы согласились, а значит завтра
Вы отправитесь в исправительную колонию для несовершеннолетних''')
        to_turma(call)

    if call.data == "norm" and count_button == 3:
        count_button += 1
        bot.send_message(call.message.chat.id, f'''Вы начали возмущаться:
- Почему я целых 2 месяца должен отбывать наказание за тот поступок, который не совершал?!
Пусть сначала следователи разберутся! Мне нельзя в тюрьму!
- Успокойтесь мистер {name1},пока ведется следствие Вы будете находится под присмотром, 
когда следователи скажут точно, то мы либо отпустим Вас, либо будет еще одно заседание суда.''')
        to_turma(call)

    # взять заточку себе
    if call.data == "only_me" and count_button == 4:
        count_button += 1
        global weapon
        weapon = 1
        bot.send_message(call.message.chat.id, ''' + ЗАТОЧКА''')
        do_time(call)

    if call.data == "good_man" and count_button == 4:
        count_button += 1
        authority1 += 1
        bot.send_message(call.message.chat.id, ''' + АВТОРИТЕТ
Теперь за вас смогут поручиться в случае чего.''')
        do_time(call)

    if call.data == "ban" and count_button == 4:
        count_button += 1
        bot.send_message(call.message.chat.id, '''Теперь вы находитесь под защитой охраны, возможно из-за 
данного поступка дело раскроется быстрее(детектив поймет, что у вас есть желание сотрудничать)''')
        do_time(call)

    if call.data == "need" and count_button == 5:
        count_button += 1
        weapon = 0
        bot.send_message(call.message.chat.id, '''Значит есть. ХА ну ты и лох!
Вас прижали к стене и обыскали''')
        bot.send_message(call.message.chat.id, '''У ВАС ЗАБРАЛИ ЗАТОЧКУ''')

    if call.data == "no_need" and count_button == 5:
        count_button += 1
        bot.send_message(call.message.chat.id, '''Да без проблем, бро.''')

    if call.data == 'help' and count_button == 5:
        count_button += 1
        bot.send_message(call.message.chat.id, '''-Отвали от него
- Кто там пискнул! Тоже хочешь по зубам получить!''')
        if luck1 >= 4:
            bot.send_message(call.message.chat.id, '''ВЫСОКИЙ УРОВЕНЬ УДАЧИ
- Смешной ты, я сказал отвали от него! - Вы вмазали парнь кулоком в солнечное сплетение. 
Минуты не прошло, как его уже не было''')
            health1 += 1
            bot.send_message(call.message.chat.id, '''+ ЗДОРОВЬЕ''')
        else:
            bot.send_message(call.message.chat.id, '''Из-за драки вас отправили в карцер''')

    if call.data == 'not_help' and count_button == 5:
        count_button += 1
        bot.send_message(call.message.chat.id, '''-Эй ты! Куда пошел! Я еще тебя не потряс''')


# БУДУЩЕЕ
def first_ask_future(message):
    keyboard = types.InlineKeyboardMarkup()
    # кнопка 1
    key_hi = types.InlineKeyboardButton(text=f'"Привет, я {name1}"', callback_data='hi')
    keyboard.add(key_hi)
    # кнопка 2
    key_molchat = types.InlineKeyboardButton(text='промолчать*', callback_data='molchat')
    keyboard.add(key_molchat)
    question = "Одноклассник: Привет, я Кевин, как тебя зовут?"
    bot.send_message(message.chat.id, text=question, reply_markup=keyboard)


# БУДУЩЕЕ
def protest_ask_future(message):
    keyboard = types.InlineKeyboardMarkup()
    # кнопка 1
    key_ploh = types.InlineKeyboardButton(text=f'да', callback_data='ploh')
    keyboard.add(key_ploh)
    # кнопка 2
    key_norm = types.InlineKeyboardButton(text='нет', callback_data='norm')
    keyboard.add(key_norm)
    # вопрос
    question = f"{name1}, Вы согласны с решением суда?"
    bot.send_message(message.chat.id, text=question, reply_markup=keyboard)


# БУДУЩЕЕ
def to_turma(call):
    bot.send_message(call.message.chat.id, '''Вот вы уже едите в автобусе с заключенными. Вы думаете, что нужно с кем-то познакомиться,
чтобы быть под защитой другого.''')
    global authority1
    if authority1 >= 3:
        bot.send_message(call.message.chat.id, '''ВЫСОКИЙ УРОВЕНЬ АВТОРИТЕТА
Вы познакомились с Томом. Его посадили за незаконную перевозку запрещенных препаратов заграницу.
Вообще он оказался довольно хорошим человеком и сам предложил держаться вместе.''')
        turma(call)

    else:
        bot.send_message(call.message.chat.id, '''НИЗКИЙ УРОВЕНЬ АВТОРИТЕТА
Оказывается заключенные не особо добрые люди.''')
        turma(call)


def turma(call):
    global luck1
    if luck1 >= 3:
        bot.send_message(call.message.chat.id, '''ВЫСОКИЙ УРОВЕНЬ УДАЧИ
Вам повезло, вы с Томом попали в одну камеру и мотать срок будет не так скучно.''')
        zatochka(call)
    else:
        bot.send_message(call.message.chat.id, '''НИЗКИЙ УРОВЕНЬ УДАЧИ
Вы в камере одни, мотать срок будет невозможно скучно''')
        zatochka(call)


def zatochka(call):
    keyboard = types.InlineKeyboardMarkup()
    # кнопка 1
    key_only_me = types.InlineKeyboardButton(text=f'Оставите себе', callback_data='only_me')
    keyboard.add(key_only_me)
    # кнопка 2
    key_good_man = types.InlineKeyboardButton(text='Отнесете блатным', callback_data='good_man')
    keyboard.add(key_good_man)
    # кнопка 3
    key_good_man = types.InlineKeyboardButton(text='Отнесете охране', callback_data='ban')
    keyboard.add(key_good_man)
    # вопрос
    question = "Во время прогулки вы нашли заточку, что будете с не делать?"
    bot.send_message(call.message.chat.id, text=question, reply_markup=keyboard)


def do_time(call):
    bot.send_message(call.message.chat.id, '''Прошел уже месяц отсидки, а про расследование все тихо. Как оказалось в 
тюрьме не так уж и много развлечений. Можно читать книги либо ходить в качалку, куда вы сейчас и направились.''')
    if weapon != 1:
        bot.send_message(call.message.chat.id, '''Вас осанавливает парень''')
        no_name(call)
    else:
        bot.send_message(call.message.chat.id, '''В углу вы видите как какой-то здоровяк прижал паренька''')
        no_name2(call)


def no_name(call):
    keyboard = types.InlineKeyboardMarkup()
    # кнопка 1
    key_need = types.InlineKeyboardButton(text='У меня есть.', callback_data='need')
    keyboard.add(key_need)
    # кнопка 2
    key_no_need = types.InlineKeyboardButton(text='Я пацифист', callback_data='no_need')
    keyboard.add(key_no_need)
    # вопрос
    question = "Эй! Парень, нужна заточка?"
    bot.send_message(call.message.chat.id, text=question, reply_markup=keyboard)


def no_name2(call):
    keyboard = types.InlineKeyboardMarkup()
    # кнопка 1
    key_help = types.InlineKeyboardButton(text='Помочь парню', callback_data='help')
    keyboard.add(key_help)
    # кнопка 2
    key_not_help = types.InlineKeyboardButton(text='Пройти мимо', callback_data='not_help')
    keyboard.add(key_not_help)
    # вопрос
    question = "Хотите вмешаться?"
    bot.send_message(call.message.chat.id, text=question, reply_markup=keyboard)


# ПРОШЛОЕ
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
        bot.send_message(call.message.chat.id, '''Вы скитаетесь в поисках работы вот уже несколько часов.
Самая выгодная работа, которую вам предложили, это уборка местной конюшни. 
Однако, по какой-то причине вам она не понравилась... 
Продолжая бродить, вы замечаете попугайчика, который вывихнул 
крыло и запутался в ветках дерева. Напишите /save''')
    # ПРОШЛОЕ, выбор спасти попугая
    if call.data == "save_parrot" and count_button == 2:
        count_button += 1
        bot.send_message(call.message.chat.id, '''Вы очень добрый человек! Вы спасли попугайчику жизнь. 
Теперь у вас появился верный друг и прибавилось уважение остальных! Однако во время спасения, вы грохнулись с дерева.
Повезло, что отделались только ушибами. Напишите /continue''')
        if health2 >= 1:
            health2 -= 1
        bot.send_message(call.message.chat.id, f'''Ваши статы на данный момент:
Здоровье - {health2},
Авторитет - {authority2 + 1}''')
    # ПРОШЛОЕ, выбор съесть попугая
    if call.data == "eat_parrot" and count_button == 2:
        count_button += 1
        bot.send_message(call.message.chat.id, '''"Ну, сейчас тяжелые времена" - подумали вы. 
Свернув попугаю шею, вы отпраляетесь на поиски ночлега. 
Теперь у вас есть ужин, а также запятнанная совесть и осуждение окружающих. Напишите /continue''')
        if authority2 >= 1:
            authority2 -= 1
        bot.send_message(call.message.chat.id, f'''Ваши статы на данный момент:
Авторитет - {authority2}''')


# ПРОШЛОЕ
def last_friend_parrot(message):
    keyboard = types.InlineKeyboardMarkup()
    # кнопка «Будущее»
    key_future = types.InlineKeyboardButton(text=f'Спасти попугайчика!', callback_data='save_parrot')
    # добавление кнопки в клавиатуру
    keyboard.add(key_future)
    # кнопка «Прошлое»
    key_ancient = types.InlineKeyboardButton(text='Забрать попугайчика и поужинать им', callback_data='eat_parrot')
    keyboard.add(key_ancient)
    question = "Как вы поступите?"
    bot.send_message(message.chat.id, text=question, reply_markup=keyboard)

# ПРОШЛОЕ
def last_korabl(message):
    bot.send_message(message.chat.id, "Так или иначе, сегодня вам опять не повезло с работой :(."
                                           " Ищя себе ночлег, вы бродите по улицам ночного острова."
                                      " Неожиданно, на вас кто-то нападает со спины!")
    global luck2
    if luck2 < 2:
        bot.send_message(message.chat.id, " НИЗКИЙ УРОВЕНЬ УДАЧИ."
                                          "К сожалению, вы не успели увернуться от атаки."
                                          "Противник пронзает нож вам прямо в сердце."
                                          "Печально; ваша история закончилась, не успев начаться")
    else:
        bot.send_message(message.chat.id, "ВЫСОКИЙ УРОВЕНЬ УДАЧИ."
                                          "Вот это реакция! Вы мастерски увернулись от атаки и уже начали бежать в "
                                          "противоположную от маньяка сторону, но не тут то было. Человек хватает вас"
                                          " за плечо. Мысленно попрощавшись с жизнью, вы готовитесь к худшему. Однако"
                                          " нападавший больше не стремится навредить вам."
                                          " 'Неплохая реакция' - с удивлением произносит человек - "
                                          "'Именно такие люди нам нужны'. Не успев понять что происходит, вы ощущаете"
                                          "сильную боль в затылке и теряете сознание. " )
        bot.send_message(message.chat.id, "Вы резко открываете глаза. Все воспоминания о вчерашнем дне перемешаны. "
                                          "Пока вы преходите в себя, вы оглядываетесь по сторонам. "
                                          "Вы попали в трюм.")


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

bot.polling()
