# Imports
import calendar
from dataclasses import dataclass
from datetime import datetime, time, timedelta
from dateutil import tz
from dateutil.relativedelta import relativedelta


@dataclass
class Raid:
    day: int
    time: time
    command: str

    @property
    def day_name(self):
        return calendar.day_name[self.day]


def get_next_raid_week_reset_date(raid_tz: str, reset_weekday: int) -> datetime:
    """
    This will return the reset/start date for next week's raid.

    This is written in such a way to allow the main signup generation to be run as soon as at least one of the raids is
    complete in order to generate the signup(s) for next week.

    Examples:
    The examples below are for raid week reset/start on Tuesday (reset_weekday).

    If today is Friday Oct 11 2024, it will return Tuesday Oct 15, 2024.
    If today is Monday Oct 14 2024, it will return Tuesday Oct 15, 2024.
    If today is Tuesday Oct 15, 2024, it will return Tuesday Oct 15, 2024.
    If today is Wednesday Oct 16, 2024, it will return Tuesday Oct 22, 2024.
    """
    utc_now = datetime.now(tz.UTC)
    raid_tz_now = utc_now.astimezone(tz.gettz(raid_tz))
    next_raid_week_reset_date = raid_tz_now + relativedelta(weekday=reset_weekday)
    return next_raid_week_reset_date


def get_raid_time_utc(raid: Raid, raid_week_reset_date: datetime) -> datetime:
    raid_time = raid_week_reset_date + relativedelta(weekday=raid.day,
                                                     hour=raid.time.hour,
                                                     minute=raid.time.minute,
                                                     second=0,
                                                     microsecond=0)
    raid_time_utc = raid_time.astimezone(tz.UTC)
    return raid_time_utc

