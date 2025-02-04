import telebot
import time, threading, schedule
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
bot = telebot.TeleBot("7958430002:AAE12foVhWq1WgfKisUR-ZmD73D9bPoWjAI")

@bot.message_handler(commands = ["start"])
def send_welcome(message):
    bot.send_message(message, "Hello!")

@bot.message_handler(commands = ["hello"])
def answer_hello(message):
    bot.reply_to(message, "Привет, как дела?")

@bot.message_handler(commands = ["bye"])
def bye_answer(message):
    bot.reply_to(message, "Ещё увидимся!")

@bot.message_handler(func = lambda message: True)
def info(message):
    markup = types.InlineKeyboardMarkup(row_width=3)
    markup.add(types.InlineKeyboardButton("START", callback_data = "start"),
               types.InlineKeyboardButton("HELLO", callback_data = "/hello"),
               types.InlineKeyboardButton("BYE", callback_data = "/bye"))
    bot.reply_to(message, "Я не знаю такой команды, но у меня есть другие команды:", reply_markup = markup)

def beep(chat_id) -> None:
    """Send the beep message."""
    bot.send_message(chat_id, text='Beep!')


@bot.message_handler(commands=['set'])
def set_timer(message):
    args = message.text.split()
    if len(args) > 1 and args[1].isdigit():
        sec = int(args[1])
        schedule.every(sec).seconds.do(beep, message.chat.id).tag(message.chat.id)
    else:
        bot.reply_to(message, 'Usage: /set <seconds>')


@bot.message_handler(commands=['unset'])
def unset_timer(message):
    schedule.clear(message.chat.id)


if __name__ == '__main__':
    threading.Thread(target=bot.infinity_polling, name='bot_infinity_polling', daemon=True).start()
    while True:
        schedule.run_pending()
        time.sleep(1)

bot.polling(none_stop=True)
