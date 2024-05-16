import imaplib
import quopri
from datetime import datetime
import re
import time
import os


class ReportGenerator:
    def __init__(self, imap_server, username, password):
        self.imap_server = imap_server
        self.username = username
        self.password = password

        self.connect_to_server()
        print(1)
    def connect_to_server(self):
        self.server = imaplib.IMAP4_SSL(self.imap_server)
        self.server.login(self.username, self.password)
        self.server.select('support')
        print(2)
    def get_report_text(self, id):
        # Получение темы письма
        subject = self.server.fetch(id, '(BODY.PEEK[HEADER.FIELDS (SUBJECT)])')[1][0][1].strip()
        subject = quopri.decodestring(subject.decode('utf-8')).decode('utf-8')
        print(3)
        # Поиск информации в теле письма
        body = self.server.fetch(id, '(RFC822)')[1][0][1]
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
        report_text = f"""
Заявка: {request_id_num}
Рабочее задание: {task_id}
Приоритет: {priority}
Пришла:{received_time}
Принята:{received_time}
Закрыта: 
"""
        time.sleep(15)
        return report_text

    def save_report_to_file(self, report_text):
        with open('report.txt', 'a') as f:
            f.write(report_text)
            f.write('\n\n')

    def clear_report_file(self):
        now = datetime.now()
        if now.hour == 20 and now.minute == 0:
            try:
                os.remove('report.txt')
                print("Файл report.txt очищен.")
            except FileNotFoundError:
                print("Файл report.txt не найден.")

    def run(self):
        while True:
            try:
                # Получение новых писем
#                response, data = self.server.uid('search', 'ALL')
                response, data = self.server.search(None, '(UNSEEN)')
                new_ids = data[0].split()

                # Обработка каждого нового письма
                for id in new_ids:
                    report_text = self.get_report_text(id)
                    self.save_report_to_file(report_text)
                    self.server.uid('STORE', id, '+FLAGS', '\\Seen')
            except Exception as e:
              print(f"Ошибка: {e}")
            self.clear_report_file()
            time.sleep(15)
if __name__ == '__main__':
    imap_server = '***'
    username = '***'
    password = '***'

    report_generator = ReportGenerator(imap_server, username, password)
    report_generator.run()
