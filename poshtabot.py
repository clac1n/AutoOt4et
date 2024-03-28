import imaplib
import quopri
from datetime import datetime
import re
import time
import telebot

# IMAP4 сервер
imap_server = 'IMAP1'

# Логин и пароль
username = 'LOGIN1'
password = 'PASSWORD1'

# Подключение к серверу
server = imaplib.IMAP4_SSL(imap_server)
server.login(username, password)

# Выбор папки "Входящие"
server.select('support')

report_file = 'report.txt'

# Токен бота
bot_token = 'TOKEN1'

# Создание экземпляра бота
bot = telebot.TeleBot(bot_token)

# Обработчик команды /report_start
@bot.message_handler(commands=['report_start'])
def start_report(message):
    # Поиск непрочитанных писем
    result, ids = server.search(None, '(UNSEEN)')

    # Обработка непрочитанных писем
    for id in ids[0].split():
        # Получение информации из письма
        report_text = get_report_text(id)

        # Отправка отчета в Telegram
        bot.send_message(message.chat.id, report_text)

# Функция для получения текста отчета
def get_report_text(id):
    # Получение темы письма
    subject = server.fetch(id, '(BODY.PEEK[HEADER.FIELDS (SUBJECT)])')[1][0][1].strip()
    subject = quopri.decodestring(subject.decode('utf-8')).decode('utf-8')

    # Поиск информации в теле письма
    body = server.fetch(id, '(RFC822)')[1][0][1]
    body = body.decode('utf-8')

        # Заявка
    request_id_num = None
    try:
        request_id_num = re.findall(r">(?<!\d)\d{7}(?!\d)<", body)[0]
    except IndexError:
        request_id_num =  "Не определенно"
        
    # Рабочее задание
    task_id = None
    try:
        task_id= re.findall(r'>(?<!\d)\d{8}(?!\d)<', body)[0]
    except IndexError:
        task_id =  "Не определенно"
        
    # Приоритет
    priority = None
    try:
        priority = re.findall(r'\s\d\s-', body)[0]
    except IndexError:
        priority = "Не определенно"
        
    # Время получения письма
    received_time = None
    try:
        received_time = re.findall(r'\s\d{2}:\d{2}', body)[0]
    except IndexError:
        received_time =  "Не определенно"

    if "1" in priority:
        priority = "1 - Критический"
    elif "2" in priority:
        priority = "2 - Высокий"
    elif "3" in priority:
        priority = "3 - Средний"
    elif "4" in priority:
        priority = "4 - Низкий"
    else:
        priority = "Не найдено"
    
    request_id_num = request_id_num.replace(">", "").replace("<", "")
    task_id = task_id.replace(">", "").replace("<","")
    # Подстановка значений в шаблон
    report_text = (f"""
    Заявка: {request_id_num}
Рабочее задание: {task_id}
Приоритет: {priority}
Пришла: {received_time}
Принята: {received_time}
Закрыта: 
    """)
    time.sleep(15)

    return report_text

# Запуск бота
bot.polling()
