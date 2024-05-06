import telebot
import re
#from script import server, get_report_text

# Токен бота
bot_token = '***'

# Создание экземпляра бота
bot = telebot.TeleBot(bot_token)

# Обработчик сообщений
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    request_id_num = message.text
    report_text = get_report_from_file(request_id_num)

    if report_text:
        bot.send_message(message.chat.id, report_text)
    else:
        bot.send_message(message.chat.id, f'Отчет для заявки {request_id_num} не найден.')

# Функция для получения отчета из файла

def get_report_from_file(request_id_num):
    with open('report.txt', 'r') as f:
        for line in f:
            if line.startswith('Заявка: ') and request_id_num in line:
                report_text = ''
                matching_line = line
                report_text += f"{matching_line.strip()}\n"
                for next_line in f:
                    if next_line.startswith('Заявка: '):
                        break
                    report_text += next_line
                return report_text
    return None

# Запуск бота
bot.polling()
