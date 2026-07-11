import os
from dotenv import load_dotenv
import telebot
import requests
from start_bd import *
from subject_bd import *
from topic_bd import *
from test_bd import *
from telebot import types


load_dotenv()
TOKEN = os.getenv('TOKEN')

if not TOKEN:
    print('Внимание: TELEGRAM_TOKEN не задан. Установите переменную окружения перед запуском.')
else:
    bot = telebot.TeleBot(TOKEN)
    print('Bot object created (запущен)')


flag = True
session_users = {}


@bot.message_handler(commands=['s', 'start'])
def start_bot(message):
     bot.send_message(message.chat.id, '''Добро пожаловать в бота который бесплатно 
поможет подготовиться к ОГЕ или ЕГЕ, или просто подтянит твои знания по школьной програме
чтоб понять что делать и как запустить бота напиши команду 
/m, /menu - эта команда открывает меню действий которые ты можешь сделать''')


@bot.message_handler(commands=['m', 'menu'])
def start_menu(message):
    bot.send_message(message.chat.id, '''/m, /menu - меню команд,
/c, /cancle - прерывание действия,
/s, /subject - выбор предмета''')


@bot.message_handler(commands=['c', 'cancle'])
def start_cancle(message):
    session_users[message.chat.id] = {}


@bot.message_handler(commands=['s', 'subject'])
def start_subject(message):
    subject = look_subject()
    keyboard = types.InlineKeyboardMarkup()
    for i in subject:
        button = types.InlineKeyboardButton(text=f'{i}', callback_data=f'sub_{i}')
        keyboard.add(button)

    bot.send_message(message.chat.id, 'Выберите предмет', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('sub_')) 
def subjects_choices(call):
    chosen_subject = call.data.replace('sub_', '')
    bot.send_message(call.message.chat.id, f'Вот темы из предмета {chosen_subject}:')
    bot.answer_callback_query(call.id)
    # bot.edit_message_reply_markup(
    #     chat_id=call.message.chat.id,
    #     message_id=call.message.message_id,
    #     reply_markup=None
    # )

    id_subject = look_id_subject(subject=chosen_subject)
    topics = look_topic_questions(subject_id=id_subject) #-------
    if topics:
        keyboard = types.InlineKeyboardMarkup()
        for i in topics:
            button = types.InlineKeyboardButton(text=f'{i}', callback_data=f'top_{i}')
            keyboard.add(button)

        bot.send_message(call.message.chat.id, 'Выберите тему', reply_markup=keyboard)

    if call.message.chat.id not in session_users:
        session_users[call.message.chat.id] = {'start_topic': id_subject}
    else: 
        session_users[call.message.chat.id]['start_topic'] = id_subject


@bot.callback_query_handler(func=lambda call: call.data.startswith('top_')) 
def chosens_topics(call):
    print(session_users)
    chosen_topic = call.data.replace('top_', '')
    # bot.send_message(call.message.chat.id, f'Вот выбранная тема {chosen_topic}:')
    bot.answer_callback_query(call.id)
    if session_users.get(call.message.chat.id) and session_users.get(call.message.chat.id).get('start_topic'):
        bot.send_message(call.message.chat.id, f'Вот теория по выбранной теме: {look_topic_theory(subject_id=session_users[call.message.chat.id]['start_topic'])}:')
        keyboard = types.InlineKeyboardMarkup()
        for i in ('да', 'нет'):
            button = types.InlineKeyboardButton(text=f'{i}', callback_data=f'que_{i}')
            keyboard.add(button)
        bot.send_message(call.message.chat.id, 'Хотите сделать задания по этой теме?', reply_markup=keyboard)
        subjects_id = session_users.get(call.message.chat.id).get('start_topic')
        session_users[call.message.chat.id] = {'start_topic_1': look_topic_id(subject_id=subjects_id, title=chosen_topic)}
    else:
        print(34343443)

@bot.callback_query_handler(func=lambda call: call.data.startswith('que_')) 
def strat_test(call):
    chosen_topic = call.data.replace('que_', '')
    chat_id = call.message.chat.id

    if chosen_topic == 'да' and chat_id in session_users and session_users[chat_id].get('start_topic_1'):
        topic = session_users[chat_id]['start_topic_1']
        test_dict = look_questions_in_test(topic) # Получаем словарь {вопрос: ответ}
        chat_id = call.message.chat.id
        print(1)
        
        if not test_dict:
            bot.send_message(chat_id, "В этой теме пока нет вопросов.")
            bot.answer_callback_query(call.id)
            return

        # Переводим ключи-вопросы в список, чтобы брать их по индексу
        questions_list = list(test_dict.keys())
        first_question = questions_list[0]
        
        # Сохраняем в сессию: сам список вопросов, индекс текущего вопроса (0) и текст текущего вопроса
        session_users[chat_id]['start_test'] = questions_list
        session_users[chat_id]['current_index'] = 0
        session_users[chat_id]['question'] = first_question
        
        # Сразу пишем пользователю первый вопрос
        bot.send_message(chat_id, f"Тест начался!\n\nВопрос №1: {first_question}")




    # if chosen_topic == 'да' and call.message.chat.id in session_users and session_users[call.message.chat.id].get('start_topic_1'):
    #     bot.send_message(call.message.chat.id, f'{look_questions_in_test(session_users[call.message.chat.id]['start_topic_1'])}')
    #     test = look_questions_in_test(session_users[call.message.chat.id]['start_topic_1'])
    #     chat_id = call.message.chat.id
    #     if chat_id not in session_users:
    #         session_users[chat_id] = {}
    #     session_users[chat_id]['start_test'] = (test, 10101010)
        
    #     print(session_users)





        # if session_users[call.message.chat.id]:
        #     session_users[call.message.chat.id]['start_test'] = (test, 10101010)
        # else: 
        #     session_users[call.message.chat.id] = {'start_test': (test, 10101010)}
    # bot.send_message(call.message.chat.id, f'Вот выбранная тема {chosen_topic}:')


@bot.message_handler(func=lambda message: message.chat.id in session_users and session_users[message.chat.id].get('start_test'))
def f(message):
    print("Хэндлер обработки ответов вызван!")
    chat_id = message.chat.id
    user_session = session_users[chat_id]
    
    # Проверяем, задан ли сейчас вопрос пользователю
    if not user_session.get('question'):
        return

    current_question = user_session['question']
    questions_list = user_session['start_test']
    current_index = user_session['current_index']
    
    # 1. Получаем правильный эталонный ответ из вашей функции/БД
    correct_answer = look_answer_in_test(question=current_question)
    
    # 2. Отправляем запрос в Ollama (phi3) для проверки ответа пользователя
    bot.send_message(chat_id, "Проверяю ваш ответ, подождите...")
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "deepseek-r1",
                "prompt": f"""Ты — строгий, но поддерживающий преподаватель. Твоя задача — проверить ответ ученика на основе эталонного ответа.

КОНТЕКСТ:
- Вопрос: "{current_question}"
- Эталонный (правильный) ответ: "{correct_answer}"
- Ответ ученика для проверки: "{message.text}"

ИНСТРУКЦИЯ ДЛЯ ОТВЕТА:
1. Оценка: Начни ответ с четкого вердикта: "✅ Верно" (если суть ответа правильная) или "❌ Ошибка" (если ответ неверный или неполный). Если ответ верный, похвали ученика (например: "Ты молодец!", "Отличная работа!").
2. Анализ: Если допущена ошибка, подробно объясни, что именно ученик указал неверно или какую важную деталь упустил.
3. Правильный разбор: Напиши, как звучит правильный ответ, и кратко объясни логику (почему именно так).

Пиши на русском языке, будь лаконичен, используй абзацы для читаемости.""",
                "stream": False
            },
            timeout=300 # Защита от вечного зависания, если Ollama долго думает
        )
        ai_response = response.json().get('response', 'Не удалось получить оценку от ИИ.')
        bot.send_message(chat_id, ai_response)
    except Exception as e:
        print(f"Ошибка Ollama: {e}")
        bot.send_message(chat_id, "Ошибка при обращении к нейросети.")

    # 3. Переходим к следующему вопросу
    next_index = current_index + 1
    
    if next_index < len(questions_list):
        # Если вопросы еще есть — берем следующий
        next_question = questions_list[next_index]
        user_session['current_index'] = next_index
        user_session['question'] = next_question
        
        bot.send_message(chat_id, f"Вопрос №{next_index + 1}: {next_question}")
    else:
        # Если вопросы закончились — очищаем состояние теста
        bot.send_message(chat_id, "🎉 Поздравляю! Вы прошли весь тест по этой теме.")
        user_session.pop('start_test', None)
        user_session.pop('current_index', None)
        user_session.pop('question', None)
        user_session[chat_id] = {}



#     print(111111)
#     chat_id = message.chat.id  
#     test = session_users[chat_id]['start_test']
#     if isinstance(test, tuple) and session_users[chat_id].get('question'):
#         test = test[0]
#         session_users[chat_id]['start_test'] = test
#         bot.send_message(message.chat.id, test.key()[0])
#         session_users[message.chat.id]['question'] = test.key()[0]
#     elif session_users[message.chat.id].get('question'):
#         question = session_users[message.chat.id].get('question')
#         answer = look_answer_in_test(question=question)
#         response = requests.post(
#             "http://localhost:11434/api/generate",
#             json={
#                 "model": "phi3",
#                 "prompt": f'''смотри ты должен проверить ответ и дать развернутый ответ если чтото гдето не так и объяснить почему это не так
# вот вопрос - {question} вот точный ответ на него в нем нет ошибки - {answer} а вот ответ который ты должен проверить и в котором может быть ошибка - {message.text}
# и оцени ответ который может быть не правильным если он верный так и напиши что он верный и напиши чтото еще по типу ты молодец если нет то напиши почему нет и как будет верно и почему ''',
#                 "stream": False
#             }
#         )

#         print(response.json()['response'])
#         bot.send_message(message.chat.id, response.json()['response'])






@bot.message_handler(func=lambda x: True)
def eco_all(message):
    print(1)
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "deepseek-r1",
            "prompt": message.text,
            "stream": False
        }
    )

    print(response.json()['response'])
    bot.send_message(message.chat.id, response.json()['response'])


while flag:
    try:
        bot.polling(none_stop=True)
    except Exception as _e:
        print(_e)

# ollama run phi3