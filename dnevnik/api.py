from dnevnik.client import *
from dnevnik.cache import *
from dnevnik.object import *
from dnevnik.util import *


class DnevnikApi:

    def __init__(self, credentials: Credentials):
        self.__credentials = credentials
        self.rest_client = self.prepare_client(True)
        self.schedule_cache = Cache(60, False)

    def get_day_lessons(self, day: WeekWorkDay, week_offset: WeekOffset = WeekOffset.get_by_offset(0)):
        return self.get_lesson_by_date(get_week_day_date(day.ordinal, week_offset.get_week_date()))

    def get_lesson_by_date(self, _date: date) -> {SchoolDay, bool, str}:
        cache_key = _date.isoformat()

        if self.schedule_cache[cache_key] is not None:
            return self.schedule_cache[cache_key], True, "временное хранение"

        lessons_response = self.rest_client.request_lessons(_date)
        if 200 < lessons_response.status_code < 500 and self.rest_client.is_olden():
            rest_client = self.prepare_client()
            if rest_client is None:
                return self.schedule_cache.data.get(cache_key), True, "ошибка получения данных"
            else:
                self.rest_client = rest_client
                lessons_response = self.rest_client.request_lessons(_date)

        if lessons_response.status_code != 200:
            return self.schedule_cache.data.get(cache_key), True, "ошибка получения данных"

        day = SchoolDay(lessons_response.json())
        self.schedule_cache[cache_key] = day

        return day, False, None

    def prepare_client(self, first: bool = False) -> DnevnikRestClient | None:
        try:
            if first:
                cached = read_auth_cache()
                if cached is not None:
                    print("[Dnevnik] Restoring auth data...")
                    return DnevnikRestClient(*cached)

            print("[Dnevnik] Requesting cookies...")
            cookies = DnevnikWebdriver.fetch_cookies(*self.__credentials)
            print("[Dnevnik] Fetching cookies...")
            write_auth_cache(cookies["profile_id"], cookies["aupd_token"])
            return DnevnikRestClient(cookies["profile_id"], cookies["aupd_token"])
        except Exception as e:
            print("[Dnevnik] Error while fetching cookies:", e)
            return None
