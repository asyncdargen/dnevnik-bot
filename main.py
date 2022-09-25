from os import getenv as env

from schedule import *
from telegram import *

DEFAULT_KEYBOARD = reply_keyboard(
    *[day.display.upper() for day in WeekWorkDay.values[5:9]], 3,
    "Расписание", "Звонки", 2
)


def main():
    api = DnevnikApi(Credentials(
        env("MOS_LOGIN"),
        env("MOS_PASSWORD")
    ))
    bot = create_bot(env("TELEGRAM_TOKEN"))

    register_schedule_handlers(api, bot)

    @bot.message_handler(commands=["start"])
    def on_start(message: Message):
        bot.send_text_message(message.from_user.id, "Привет это бот", markup=DEFAULT_KEYBOARD)

    bot.infinity_polling()


if __name__ == "__main__":
    main()
