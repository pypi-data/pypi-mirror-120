import logging
from datetime import datetime


class Util:

    @staticmethod
    def is_not_blank(s) -> bool:
        return bool(s and not s.isspace())

    @staticmethod
    def oneWeekOld(postDate: str, old: int = 7) -> bool:
        post = datetime.fromisoformat(postDate[:-1])
        diffDay = (datetime.now() - post).days
        return diffDay <= old

    @staticmethod
    def isOpenOrClose(state: str) -> bool:
        return state.lower() in ("open", "closed")

