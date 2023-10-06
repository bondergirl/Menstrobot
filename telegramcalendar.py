#!/usr/bin/env python3
#
# A library that allows to create an inline calendar keyboard.
# grcanosa https://github.com/grcanosa
#
"""
Base methods for calendar keyboard creation and processing.
"""

import telebot
import calendar


def prepare_callback_data(data):
    pass


def create_callback_data(action: str, year: int, month: int, day: int) -> str:
    """ Create the callback data associated to each button"""
    return ";".join([action, str(year), str(month), str(day)])


def get_month_and_year(year: int, month: int) -> str:
    cl = calendar.LocaleTextCalendar(firstweekday=0, locale=('Russian_Russia', '1251'))
    month_and_year = cl.formatmonth(year, month).split("\n")[0].strip()
    return month_and_year


def create_calendar(year: int, month: int) -> telebot.types.InlineKeyboardMarkup:
    """
    Create an inline keyboard with the provided year and month
    :param day: Day to use in the calendar, if None the current day is used.
    :param int year: Year to use in the calendar, if None the current year is used.
    :param int month: Month to use in the calendar, if None the current month is used.
    :return: Returns the InlineKeyboardMarkup object with the calendar.
    """
    day = 0
    data_ignore = create_callback_data("IGNORE", year, month, day)
    keyboard = []
    # First row - Month and Year
    cl = calendar.LocaleTextCalendar(firstweekday=0, locale=('Russian_Russia', '1251'))
    row = [telebot.types.InlineKeyboardButton(text=cl.formatmonth(year, month).split("\n")[0],
                                              callback_data=data_ignore)]
    keyboard.append(row)
    # Second row - Week Days
    row = []
    weekdays = cl.formatmonth(year, month).split("\n")[1].split(" ")
    for day in weekdays:
        row.append(telebot.types.InlineKeyboardButton(text=day,
                                                      callback_data=data_ignore))
    keyboard.append(row)
    m_calendar = calendar.monthcalendar(year, month)
    for week in m_calendar:
        row = []
        for day in week:
            if day == 0:
                row.append(telebot.types.InlineKeyboardButton(text=" ",
                                                              callback_data=data_ignore))
            else:
                row.append(telebot.types.InlineKeyboardButton(text=str(day),
                                                              callback_data=create_callback_data("DAY",
                                                                                                 year, month, day)))
        keyboard.append(row)
    # Last row - Buttons
    row = [telebot.types.InlineKeyboardButton(text="<",
                                              callback_data=create_callback_data("PREV-MONTH",
                                                                                 year, month, day)),
           telebot.types.InlineKeyboardButton(text=" ",
                                              callback_data=data_ignore),
           telebot.types.InlineKeyboardButton(text=">",
                                              callback_data=create_callback_data("NEXT-MONTH",
                                                                                 year, month, day))]
    keyboard.append(row)

    return telebot.types.InlineKeyboardMarkup(keyboard)
