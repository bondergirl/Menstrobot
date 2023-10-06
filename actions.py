import datetime
import telebot
import db
import telegramcalendar


def sql_to_date(sql_date: str) -> datetime.date:
    date_and_time = datetime.datetime.strptime(sql_date, "%Y-%m-%d")
    date_obj_str = datetime.datetime.strftime(date_and_time, "%Y-%m-%d")[::]
    date_obj = datetime.datetime.strptime(date_obj_str, "%Y-%m-%d").date()
    return date_obj


def sql_to_int(sql_date: str) -> tuple:
    date_obj = sql_to_date(sql_date)
    return "CHANGE", date_obj.year, date_obj.month, date_obj.day


class BotActions(telebot.TeleBot):
    def __init__(self, token: str):
        super().__init__(token)
        self.bot = telebot.TeleBot(token)

    def say_hi(self, message: telebot.types.Message):
        self.send_message(message.chat.id, "Я приветствую тебя!")

    def print_help(self, message: telebot.types.Message):
        self.bot.send_message(message.chat.id, f"Мой принцип: только необходимые функции.\n"
                                               f"Я не буду нагружать вопросами, чтобы общение со мной \n"
                                               f"не воспринималось как допрос, который следует отложить,\n"
                                               f"и в итоге забыть отметить цикл совсем. Внесение данных займет \n"
                                               f"не более минуты, и контроль за своим циклом перестанет быть \n"
                                               f"мучительной обязанностью.\n\n"
                                               f"Я умею:\n"
                                               f"- Регистрировать пользователя;\n"
                                               f"- Отмечать начало цикла;\n"
                                               f"- Редактировать данные о начале цикла;\n"
                                               f"- Показывать статистику циклов;\n"
                                               f"Для начала работы нажми кнопку МЕНЮ и выбери нужную команду.")

    def welcome_user(self, message: telebot.types.Message):
        users = db.BotDB(table_name="users.sql")
        user_id = str(message.from_user.id)
        user_name = str(message.from_user.first_name)
        registered_date = str(datetime.datetime.now())
        if users.db_register(user_id, user_name, registered_date):
            self.send_message(chat_id=message.chat.id,
                              text=f"Добро пожаловать, {user_name}!")
        else:
            self.send_message(message.chat.id, text=f"{user_name}, рад видеть вас снова!")
            self.show_cycle(message)

    def start_cycle(self, message: telebot.types.Message):
        markup = telebot.types.InlineKeyboardMarkup()
        today = telebot.types.InlineKeyboardButton(text="Сегодня", callback_data="today")
        yesterday = telebot.types.InlineKeyboardButton(text="Вчера", callback_data="yesterday")
        calendar = telebot.types.InlineKeyboardButton(text="Другая дата", callback_data="calendar")
        markup.add(today, yesterday)
        markup.add(calendar)
        self.send_message(message.chat.id, "Выберите дату начала нового цикла:", reply_markup=markup)

    def add_cycle(self, call: telebot.types.CallbackQuery, user_id: str, date: str):
        cycles = db.BotDB(table_name="cycles.sql")
        if cycles.db_add_cycle(user_id, date):
            self.send_message(chat_id=call.message.chat.id,
                              text=f"Данные успешно внесены: {date}\n"
                                   f"Посмотреть статистику циклов: команда /statistics")
        else:
            self.send_message(chat_id=call.message.chat.id,
                              text="Такие данные уже были в Вашем архиве.\n"
                                   "Посмотреть статистику циклов: команда /statistics")

    def custom_date(self, call: telebot.types.CallbackQuery):
        ret_data = None
        (action, year, month, day) = call.data.split(";")
        curr = datetime.date(int(year), int(month), 1)

        if action == "IGNORE":
            self.answer_callback_query(callback_query_id=call.id,
                                       text="Это не кнопка",
                                       show_alert=False)
        elif action == "DAY":
            self.edit_message_text(text=f"{call.message.text}",
                                   chat_id=call.message.chat.id,
                                   message_id=call.message.message_id)
            ret_data = datetime.date(int(year), int(month), int(day))
            self.send_message(call.message.chat.id, f"Вы выбрали дату: {ret_data}")
            self.add_cycle(call, str(call.from_user.id), str(ret_data))
        elif action == "PREV-MONTH":
            pre = curr - datetime.timedelta(days=1)
            self.edit_message_text(text=call.message.text,
                                   chat_id=call.message.chat.id,
                                   message_id=call.message.message_id,
                                   reply_markup=self.show_calendar(call, int(pre.year), int(pre.month)))
        elif action == "NEXT-MONTH":
            ne = curr + datetime.timedelta(days=31)
            self.edit_message_text(text=call.message.text,
                                   chat_id=call.message.chat.id,
                                   message_id=call.message.message_id,
                                   reply_markup=self.show_calendar(call, int(ne.year), int(ne.month)))
        elif action == "CHANGE":
            user_id = str(call.from_user.id)
            if int(month) < 10:
                month = month.zfill(2)
            if int(day) < 10:
                day = day.zfill(2)
            date_to_change = "".join([year, "-", month, "-", day])
            self.send_message(chat_id=call.message.chat.id,
                              text=f"Удаляем дату: {date_to_change}")
            cycles = db.BotDB(table_name="cycles.sql")
            if cycles.db_remove_cycle(user_id=user_id, date_to_delete=date_to_change):
                self.send_message(chat_id=call.message.chat.id,
                                  text=f"Дата успешно удалена! Внесите новую дату начала цикла: команда /start")
            else:
                self.send_message(chat_id=call.message.chat.id,
                                  text="Удалить данные не удалось")
        else:
            self.send_message(call.message.chat.id, text="Что-то пошло не так!")
        return ret_data

    def show_calendar(self, call: telebot.types.CallbackQuery, year: int = None, month: int = None):
        now = datetime.datetime.now()
        if year is None:
            year = now.year
        if month is None:
            month = now.month
        self.send_message(call.message.chat.id,
                          text="Выберите дату: " + telegramcalendar.get_month_and_year(year, month),
                          reply_markup=telegramcalendar.create_calendar(year, month))

    def show_statistics(self, message: telebot.types.Message):
        self.show_cycle(message)
        user_id = [str(message.from_user.id)]
        print(user_id)
        cycles = db.BotDB(table_name="cycles.sql")
        user_cycles = cycles.db_statistics(user_id)
        markup = telebot.types.InlineKeyboardMarkup()
        if user_cycles:
            for date in user_cycles:
                date_tuple = sql_to_int(date[0])
                date_callback = telegramcalendar.create_callback_data(action=date_tuple[0],
                                                                      year=date_tuple[1],
                                                                      month=date_tuple[2],
                                                                      day=date_tuple[3])
                markup.add(telebot.types.InlineKeyboardButton(text=date[0],
                                                              callback_data=date_callback))
            self.send_message(message.chat.id,
                              text="Ваши циклы:",
                              reply_markup=markup)
        else:
            self.send_message(message.chat.id, "Ваши данные о циклах пока пусты. Внесите первые данные командой START")

    def show_cycle(self, message: telebot.types.Message):
        user_id = str(message.from_user.id)
        cycles = db.BotDB(table_name="cycles.sql")
        last_cycle_date = cycles.db_show_last_cycle([user_id])[0][0]
        today = datetime.date.today()
        curr_cycle_days = (today - sql_to_date(last_cycle_date)).days
        self.send_message(message.chat.id, f"Сегодня {curr_cycle_days}-й день цикла.")
        self.send_message(message.chat.id, f"Дата вашего последнего цикла:\n"
                                           f"{last_cycle_date}")
