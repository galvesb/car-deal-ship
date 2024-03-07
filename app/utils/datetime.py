from datetime import datetime, timezone


def replace_timezone(date: datetime, new_timezone: timezone) -> datetime:
    return date.replace(tzinfo=new_timezone)


def utc_now() -> datetime:
    return replace_timezone(datetime.utcnow(), timezone.utc)
