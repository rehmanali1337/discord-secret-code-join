from sqlitedict import SqliteDict
from app import gvs


class UsedCodes:
    def __init__(self) -> None:
        self._file = gvs.CODES_DB
        self._db = SqliteDict(self._file, "codes", autocommit=True)
        self._key = "used_codes"

    def get_used_codes_list(self):
        try:
            return self._db[self._key]
        except KeyError:
            return []

    def add_code(self, code: str):
        prev = self.get_used_codes_list()
        prev.append(code)
        self._db[self._key] = prev

    def is_used_code(self, code: str):
        return code in self.get_used_codes_list()
