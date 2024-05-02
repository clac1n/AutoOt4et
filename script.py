import imaplib
import quopri
from datetime import datetime
import re
import time

# IMAP4 сервер
imap_server = '***'

# Логин и пароль
username = '***'
password = '***'

# Подключение к серверу
server = imaplib.IMAP4_SSL(imap_server)
server.login(username, password)

# Выбор папки "Входящие"
server.select('support')

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
        request_id_num = "Не определено"

    # Рабочее задание
    task_id = None
    try:
        task_id= re.findall(r'>(?<!\d)\d{8}(?!\d)<', body)[0]
    except IndexError:
        task_id = "Не определено"

    # Приоритет
    priority = None
    try:
        priority = re.findall(r'\s\d\s-', body)[0]
    except IndexError:
        priority = "Не определено"

    # Время получения письма
    received_time = None
    try:
        received_time = re.findall(r'\s\d{2}:\d{2}', body)[0]
    except IndexError:
        received_time = "Не определено"

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

    # Сохранение отчета в файл
    save_report_to_file(report_text)

    time.sleep(15)

    return report_text

def save_report_to_file(report_text):
    with open('report.txt', 'a') as f:
        f.write(report_text)
        f.write('\n\n')
