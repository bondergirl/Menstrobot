import datetime
import time
import telebot
import actions
import config

bot = actions.BotActions(token=config.TOKEN)


@bot.message_handler(commands=["hi"])
def say_hi(message: telebot.types.Message):
    bot.say_hi(message)


@bot.message_handler(commands=["help"])
def print_help(message: telebot.types.Message):
    bot.print_help(message)


@bot.message_handler(commands=["start"])
def start(message: telebot.types.Message):
    bot.welcome_user(message)
    bot.start_cycle(message)


@bot.message_handler(commands=["cycle"])
def get_current_cycle(message: telebot.types.Message):
    bot.show_cycle(message)


@bot.callback_query_handler(func=lambda call: call.data in ["today", "yesterday", "calendar"])
def start_new_cycle(call: telebot.types.CallbackQuery):
    user_id = str(call.from_user.id)
    today = str(datetime.date.today())
    yesterday = str(datetime.date.today() - datetime.timedelta(days=1))
    if call.data == "today":
        bot.add_cycle(call, user_id, today)
    elif call.data == "yesterday":
        bot.add_cycle(call, user_id, yesterday)
    elif call.data == "calendar":
        bot.show_calendar(call)


@bot.callback_query_handler(func=lambda call: call.data not in ["today", "yesterday", "calendar"])
def custom_date(call: telebot.types.CallbackQuery):
    bot.custom_date(call)


@bot.message_handler(commands=["change"])
def change_cycle(message):
    bot.send_message(chat_id=message.chat.id,
                     text="Выберите дату, которую хотите изменить, из статистики")
    bot.show_statistics(message)


@bot.message_handler(commands=["statistics"])
def statistics(message: telebot.types.Message):
    bot.show_statistics(message)


if __name__ == '__main__':
    try:
        bot.polling(none_stop=True)
    except Exception as err:
        print(repr(err))
        time.sleep(1)
