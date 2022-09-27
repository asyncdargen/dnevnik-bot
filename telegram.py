from telebot import *
from telebot.types import *


class TelegramBot(TeleBot):

    def __init__(self, token: str):
        super().__init__(token)

    def send_text_message(self, chat_id: int, text: str, markup: REPLY_MARKUP_TYPES = None):
        super().send_message(chat_id=chat_id, text=text, reply_markup=markup, parse_mode="HTML")

    def edit_text_message(self, chat_id: int, message_id: int, text: str, markup: REPLY_MARKUP_TYPES = None):
        super().edit_message_text(chat_id=chat_id, text=text, message_id=message_id, reply_markup=markup, parse_mode="HTML")


def create_bot(token: str):
    return TelegramBot(token)


def tag(tag, text):
    return f"<{tag}>{text}</{tag}>"


def bold(text):
    return tag("b", text)


def italic(text):
    return tag("i", text)


def strike(text):
    return tag("s", text)


def underline(text):
    return tag("u", text)


def code(text):
    return tag("code", text)


def large_code(text):
    return tag("pre", text)


def clear(text):
    return text


def words_regexp(*args):
    return "|".join(map(str, args))


def data_filter(data):
    return lambda call: call.data.startswith(data)


def reply_keyboard(*args):
    markup = ReplyKeyboardMarkup()

    buttons = list()
    weight = 2

    for arg in args:
        if type(arg) is int:
            weight = arg
            if len(buttons) > 0:
                markup.add(*buttons, row_width=weight)
                buttons.clear()
        else:
            buttons.append(KeyboardButton(arg))

    if len(buttons) > 0:
        markup.add(*buttons, row_width=weight)

    return markup


def build_list_inline_markup(*args):
    markup = InlineKeyboardMarkup()

    buttons = list()
    weight = 1

    for arg in args:
        if type(arg) is int:
            weight = arg
            if len(buttons) > 0:
                markup.add(*buttons, row_width=weight)
                buttons.clear()
        else:
            text, data = arg.split("|")
            buttons.append(InlineKeyboardButton(text, callback_data=data))

    if len(buttons) > 0:
        markup.add(*buttons, row_width=weight)

    return markup


def build_dict_inline_markup(*args):
    markup = InlineKeyboardMarkup()

    for buttons_pairs in args:
        buttons = list()
        for (name, data) in buttons_pairs.items():
            buttons.append(InlineKeyboardButton(name, callback_data=data))

        markup.add(*buttons, row_width=len(buttons_pairs))

    return markup
