from dnevnik.util import *

NOT_LESSON = ["Индивидуальный проект"]
LESSON_ALIASES = {
    "Математика": "Алгебра",
    "Обществознание": "Общество",
    "Английский язык": "Английский",
    "Практикум по русскому языку": "Русский",
    "Русский язык": "Русский",
    "Практикум по решению математических задач": "Геометрия",
    "Основы безопасности жизнедеятельности": "ОБЖ",
    "Физическая культура": "Физ-ра",
    "Создание цифровых двойников": "СЦД",
    "Основы технологий искусственного интеллекта": "ОТИИ",
    "Программирование микроконтроллеров": "ПМ",
    "Информационная безопасность": "ИБ",
}
MARK_WEIGHTS = "₀₁₂₃₄₅₆₇₈₉"


def filter_is_lesson(raw_lesson: dict) -> bool:
    return raw_lesson["type"] == "LESSON" and raw_lesson["lesson"]["subject_name"] not in NOT_LESSON


class SchoolDay:

    def __init__(self, raw: dict):
        self.timestamp = datetime.today()
        self.date = date.fromisoformat(raw["date"])
        self.week_day = WeekWorkDay.get_by_ordinal(self.date.weekday())

        self.lessons_count = 0

        def resolve_lesson(raw_lesson: dict) -> Lesson:
            self.lessons_count += 1
            return Lesson(self.lessons_count, self.date, raw_lesson)

        self.lessons = {lesson.index: lesson for lesson in map(
            resolve_lesson,
            filter(filter_is_lesson, raw["activities"])
        )}


class Mark:

    def __init__(self, value, weight):
        self.value = value
        self.weight = weight

    def __str__(self):
        return str(self.value) + (MARK_WEIGHTS[self.weight] if self.weight != 1 else "")


def resolve_homework(homework: str) -> str:
    return f" {homework}" if (homework is None or len(homework) > 0) and "не задано" not in homework.lower() else None


def resolve_lesson_name(name) -> str:
    return name if name not in LESSON_ALIASES else LESSON_ALIASES[name]


class Lesson:

    def __init__(self, index: int, _date: date, raw: dict):
        self.index = index

        self.begin_time = datetime_with_date(datetime.strptime(raw["begin_time"], "%H:%M"), _date)
        self.end_time = datetime_with_date(datetime.strptime(raw["end_time"], "%H:%M"), _date)

        self.name = resolve_lesson_name(raw["lesson"]["subject_name"])
        self.homework = resolve_homework(raw["lesson"]["homework"])

        self.marks = list(
            map(lambda raw_mark: Mark(int(raw_mark["value"]), int(raw_mark["weight"])), raw["lesson"]["marks"])
        )

    def is_now(self):
        return is_today_datetime(self.end_time) and is_in_datetime_range(self.begin_time, self.end_time)

    def is_ends(self):
        return is_today_datetime(self.end_time) and is_after_datetime(self.end_time)
