from dnevnik import *
from dnevnik.object import *
from dnevnik.util import *
from telegram import *
from main import DEFAULT_KEYBOARD


def week_keyboard(offset: int):
    return inline_keyboard(
        *[f"{day.alias.upper()}|schedule_day_{day.name}_{offset}" for day in WeekWorkDay.values[0:5]], 5,
        *[f"{offset.display}|schedule_week_{offset.offset}" for offset in exclude(
            WeekOffset.get_by_offset(offset),
            WeekOffset.get_by_offset(-offset),
            collection=WeekOffset.values.copy())]
    )


RING_SCHEDULE = [
    ["8:30", "9:15"], ["9:25", "10:10"],
    ["10:25", "11:10"], ["11:25", "12:10"],
    ["12:30", "13:15"], ["13:30", "14:15"],
    ["14:30", "15:15"]
]


def lesson_to_plain_text(day_info: {SchoolDay, bool, str}):
    day, cached, message = day_info

    str_lessons = "\n".join(map(
        lambda lesson:
        f"{lesson.index}. " +
        (underline if lesson.is_now() else strike if lesson.is_ends() else clear)(bold(lesson.name)) +
        (f" ({','.join(map(str, lesson.marks))})" if len(lesson.marks) > 0 else "") +
        (f":{large_code(lesson.homework)}" if lesson.homework is not None else ""),
        day.lessons.values()
    )) if len(day.lessons.values()) > 0 else "Уроков нет :)"

    return f"Расписание на {day.week_day.display.lower()} ({str_date_time(day.date)}):\n{str_lessons}" + \
           ("\n\n" + bold(underline(f"Загружено из кеша {str_date_time(day.timestamp)}: {message}")) if cached else "")


def register_schedule_handlers(api: DnevnikApi, bot: TelegramBot):
    def send_week_day_selector(chat_id: int, offset: int, message_id: int = None):
        if message_id is None:
            bot.send_text_message(
                chat_id=chat_id,
                text=f"Выбери день ({WeekOffset.get_by_offset(offset).display}):",
                markup=week_keyboard(offset)
            )
        else:
            bot.edit_text_message(
                chat_id=chat_id,
                message_id=message_id,
                text=f"Выбери день ({WeekOffset.get_by_offset(offset).display}):",
                markup=week_keyboard(offset)
            )

    @bot.message_handler(regexp="расписание")
    def on_schedule(message: Message):
        send_week_day_selector(message.from_user.id, 0)

    @bot.callback_query_handler(func=data_filter("schedule_previous"))
    def on_previous_query(call: CallbackQuery):
        send_week_day_selector(call.message.chat.id, int(call.data.split("_")[2]), message_id=call.message.message_id)

    @bot.callback_query_handler(func=data_filter("schedule_week"))
    def on_week_query(call: CallbackQuery):
        send_week_day_selector(call.message.chat.id, int(call.data.split("_")[2]), message_id=call.message.message_id)

    @bot.callback_query_handler(func=data_filter("schedule_day"))
    def on_day_query(call: CallbackQuery):
        day, offset = call.data.split("_")[2:4]
        bot.edit_text_message(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            markup=inline_keyboard(f"Назад|schedule_previous_{offset}"),
            text=lesson_to_plain_text(api.get_day_lessons(
                WeekWorkDay.get_by_name(day), WeekOffset.get_by_offset(int(offset))
            )),
        )

    @bot.message_handler(regexp="звонки|звонок")
    def on_message(message: Message):
        bot.send_text_message(
            message.from_user.id,
            "Звонки: \n" + "\n".join(
                [f"{i + 1}. " + bold({ring[0]} - {ring[1]}) for i, ring in enumerate(RING_SCHEDULE)]),
            markup=DEFAULT_KEYBOARD
        )

    @bot.message_handler(regexp="|".join([f"{day.display}|{day.alias}" for day in WeekWorkDay.values]))
    def on_message(message: Message):
        bot.send_text_message(
            message.from_user.id,
            lesson_to_plain_text(api.get_lesson_by_date(WeekWorkDay.get_by_name(message.text).nearest_date())),
            markup=DEFAULT_KEYBOARD
        )
