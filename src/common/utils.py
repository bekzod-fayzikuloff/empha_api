import datetime

from rest_framework.exceptions import ValidationError


def parse_datetime_qs(qs: str) -> datetime.datetime:
    try:
        return datetime.datetime.strptime(qs, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        try:
            return datetime.datetime.strptime(qs, "%Y-%m-%d")
        except ValueError:
            raise ValidationError("Not support datetime qs type")
