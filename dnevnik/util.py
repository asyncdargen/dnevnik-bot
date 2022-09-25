from datetime import *
from time import time as seconds
from typing import TypeVar

T = TypeVar('T')


def exclude(*elements: T, collection: list) -> list:
    for element in elements:
        try:
            collection.remove(element)
        except:
            pass

    return collection


class WeekWorkDay:
    size = 0
    values = list()

    def __init__(self, name, display, alias, date_getter):
        self.name = name
        self.display = display
        self.alias = alias
        self.date_getter = date_getter

        self.ordinal = WeekWorkDay.size
        WeekWorkDay.size += 1
        WeekWorkDay.values.append(self)

    @staticmethod
    def defaults():
        WeekWorkDay("MONDAY", "Понедельник", "Пн", lambda: get_week_day_date(0))
        WeekWorkDay("TUESDAY", "Вторник", "Вт", lambda: get_week_day_date(1))
        WeekWorkDay("WEDNESDAY", "Среда", "Ср", lambda: get_week_day_date(2))
        WeekWorkDay("THURSDAY", "Четверг", "Чт", lambda: get_week_day_date(3))
        WeekWorkDay("FRIDAY", "Пятница", "Пт", lambda: get_week_day_date(4))

        WeekWorkDay("TODAY", "Сегодня", "Сейчас", lambda: get_work_day_date(0))
        WeekWorkDay("TOMORROW", "Завтра", "Следущее", lambda: get_work_day_date(1))
        WeekWorkDay("AFTER_TOMORROW", "Послезавтра", "Послеследующее", lambda: get_work_day_date(2))

    @staticmethod
    def get_by_ordinal(ordinal: int):
        for day in WeekWorkDay.values:
            if day.ordinal == ordinal:
                return day

    @staticmethod
    def get_by_name(name: str):
        for day in WeekWorkDay.values:
            if name in day:
                return day

    def nearest_date(self) -> date:
        return self.date_getter()

    def __contains__(self, item) -> bool:
        return type(item) is str and (
                self.display.lower() == item.lower() or self.alias.lower() == item.lower() or self.name.lower() == item.lower())


WeekWorkDay.defaults()


class WeekOffset:
    size = 0
    values = list()

    def __init__(self, name, display, offset):
        self.name = name
        self.display = display
        self.offset = offset

        self.ordinal = WeekOffset.size
        WeekOffset.size += 1
        WeekOffset.values.append(self)

    @staticmethod
    def defaults():
        WeekOffset("PREVIOUS", "Предыдущая неделя", -1)
        WeekOffset("CURRENT", "Текущая неделя", 0)
        WeekOffset("NEXT", "Следующая неделя", 1)

    @staticmethod
    def get_by_offset(offset: int):
        for day in WeekOffset.values:
            if day.offset == offset:
                return day

    def get_week_date(self) -> date:
        current = date.today()
        current -= timedelta(weeks=-self.offset, days=current.weekday())
        return current

    def __contains__(self, item) -> bool:
        return type(item) is str and (
                self.display.lower() == item.lower() or self.name.lower() == item.lower()) or item == self.ordinal


WeekOffset.defaults()


def is_today_datetime(time: datetime) -> bool:
    return datetime.today().day == time.day


def is_after_datetime(after: datetime) -> bool:
    return after <= datetime.today()


def is_in_datetime_range(begin: datetime, end: datetime) -> bool:
    return begin <= datetime.today() <= end


def datetime_with_date(_datetime: datetime, _date: date) -> datetime:
    return _datetime.replace(day=_date.day, month=_date.month, year=_date.year)


def get_work_day_date(offset) -> date:
    day_date = date.today()
    day_date += timedelta(days=offset)

    # while day_date.weekday() > 4:
    #     day_date += timedelta(days=1)

    return day_date


def get_week_day_date(ordinal, week_start: date = date.today()) -> date:
    while week_start.weekday() != ordinal:
        week_start += timedelta(days=1)

    return week_start


def str_date_time(_datetime) -> str:
    if type(_datetime) is datetime:
        return _datetime.strftime("%H:%M %d.%m.%Y")
    elif type(_datetime) is date:
        return _datetime.strftime("%d.%m.%Y")


def millis() -> float:
    return seconds() * 1000
