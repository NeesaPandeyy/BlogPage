from datetime import datetime, timedelta

from django.utils import timezone
from django.utils.timesince import timesince


def custom_date_display(value):
    if not value:
        return ""

    now = timezone.now()
    date = (
        value
        if isinstance(value, datetime)
        else datetime.combine(value, datetime.min.time())
    )
    date_only = date.date()
    now_only = now.date()

    if date_only == now_only:
        diff = timesince(date, now)
        return f"{diff.split(',')[0]} ago"
    elif date_only == now_only - timedelta(days=1):
        return "Yesterday"
    else:
        return date.strftime("%d %B , %Y")
