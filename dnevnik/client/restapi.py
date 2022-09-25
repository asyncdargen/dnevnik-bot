from datetime import *
from requests import *

DNEVNIK_API_END_POINT = "https://dnevnik.mos.ru/mobile/api/"


class DnevnikRestClient:

    def __init__(self, profile_id: str, auth_token: str, timestamp: datetime = datetime.now()):
        self.timestamp = timestamp
        self.__auth_token = auth_token
        self.__profile_id = profile_id

    def request_lessons(self, _date: date) -> Response:
        return self.__make_get_request("schedule", {"student_id": self.__profile_id, "date": _date.isoformat()})

    def __make_get_request(self, path, query: dict = None) -> Response:
        return get(DNEVNIK_API_END_POINT + path, params=query, headers=self.__prepare_headers())

    def __prepare_headers(self) -> dict[str, str]:
        return {
            "Auth-Token": self.__auth_token,
            "Profile-Id": self.__profile_id,
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": r"application/json, text/plain, */*"
        }

    def is_olden(self) -> bool:
        return (datetime.now() - self.timestamp) > timedelta(seconds=60)
