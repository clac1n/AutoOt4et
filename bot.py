import telebot
from script import server, get_report_text

# Токен бота
bot_token = '***'

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

# Запуск бота
bot.polling()

