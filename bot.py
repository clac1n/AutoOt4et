import telebot
import re
import datetime

# Токен бота
bot_token = '***'

# Создание экземпляра бота
bot = telebot.TeleBot(bot_token)

c = chr(24)

# Обработчик сообщений
@bot.message_handler(func=lambda message: True)
def handle_message(message):
  request_id_num = message.text
  report_text = get_report_from_file(request_id_num, message.chat.id)

  if report_text:
    bot.send_message(message.chat.id, report_text)
  else:
    bot.send_message(message.chat.id, f'Отчет для заявки {request_id_num} не найден.')

# Функция для получения отчета из файла
def get_report_from_file(request_id_num, chat_id):
  current_time = datetime.datetime.now().strftime('%H:%M')
  with open('report.txt', 'r') as f:
    for line in f:
      if line.startswith('Заявка: ') and request_id_num in line[-4:]:
        report_text = ''
        matching_line = line
        report_text += f"{matching_line.rstrip()}\n"
        for next_line in f:
          # Проверка, начинается ли строка с "Закрыта:"
          if next_line.startswith('Закрыта: '):
            # Извлечение существующего текста "Закрыта:"
            closed_line = next_line.rstrip()
            # Разделение текста "Закрыта:" и времени
            closed_text, closed_time = closed_line.split(':')
            # Обновление времени закрытия
            updated_closed_line = f"Закрыта: {current_time}"
            # Объединение обновленного текста "Закрыта:" и остальной части отчета
            report_text += f"{updated_closed_line}\n"
          else:
            report_text += next_line
        return report_text
  return None

# Запуск бота
bot.polling()
