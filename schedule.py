from dnevnik import *
from dnevnik.util import *
from main import DEFAULT_KEYBOARD
from telegram import *


def register_schedule_handlers(api: DnevnikApi, bot: TelegramBot):
    def send_week_keyboard(chat_id, offset: int, message_id: int = None):
        week_offset = WeekOffset.get_by_offset(offset)
        markup = build_dict_inline_markup(
            {day.display.upper(): f"schedule_day_{day.ordinal}_{offset}" for day in WeekWorkDay.values[5:9]},
            {day.alias.upper(): f"schedule_day_{day.ordinal}_{offset}" for day in WeekWorkDay.values[0:5]},
            {offset.display.upper(): f"schedule_week_{offset.offset}" for offset in exclude(
                WeekOffset.get_by_offset(offset),
                WeekOffset.get_by_offset(-offset),
                collection=WeekOffset.values.copy())}
        )
        message = f"Выбери день ({week_offset.display}):"
        if message_id:
            bot.edit_text_message(chat_id, message_id, message, markup)
        else:
            bot.send_text_message(chat_id, message, markup)

    @bot.callback_query_handler(func=data_filter("schedule_previous"))
    def on_previous_query(call: CallbackQuery):
        send_week_keyboard(call.from_user.id, int(call.data.split("_")[2]), message_id=call.message.message_id)

    @bot.callback_query_handler(func=data_filter("schedule_week"))
    def on_week_query(call: CallbackQuery):
        send_week_keyboard(call.from_user.id, int(call.data.split("_")[2]), message_id=call.message.message_id)

    @bot.callback_query_handler(func=data_filter("schedule_day"))
    def on_day_query(call: CallbackQuery):
        week_day, offset = map(int, call.data.split("_")[2:4])
        day, cached, text = api.get_day_lessons(WeekWorkDay.get_by_ordinal(week_day), WeekOffset.get_by_offset(offset))

        str_lessons = "\n".join(map(
            lambda lesson:
            f"{lesson.index}. " +
            (underline if lesson.is_now() else strike if lesson.is_ends() else clear)(bold(lesson.name)) +
            (f" ({', '.join(map(str, lesson.marks))})" if len(lesson.marks) > 0 else "") +
            (f":{large_code(lesson.homework)}" if lesson.homework is not None else ""),
            day.lessons.values()
        )) if len(day.lessons.values()) > 0 else "Уроков нет :)"

        bot.edit_text_message(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            markup=build_dict_inline_markup({"Назад": f"schedule_week_{offset}"}),
            text=f"Расписание на {day.week_day.display.lower()} ({str_date_time(day.date)}):\n{str_lessons}\n\n" +
                 (bold(underline(f"Загружено из кеша {str_date_time(day.timestamp)}: {text}")) if cached else "")
        )

    @bot.message_handler(regexp=words_regexp("звонки", "звонок"))
    def on_message(message: Message):
        bot.send_text_message(
            message.from_user.id,
            "Звонки: \n" + "\n".join(
                [f"{i + 1}. {ring}" for i, ring in enumerate(map(lambda ring: bold(ring[0] + " - " + ring[1]), [
                    ["8:30", "9:15"], ["9:25", "10:10"], ["10:25", "11:10"], ["11:25", "12:10"],
                    ["12:30", "13:15"], ["13:30", "14:15"], ["14:30", "15:15"]
                ]))]),
            markup=DEFAULT_KEYBOARD
        )

    @bot.message_handler(regexp=words_regexp("расписание", "дз", "домашка"))
    def on_schedule(message: Message):
        send_week_keyboard(message.from_user.id, 0, None)
