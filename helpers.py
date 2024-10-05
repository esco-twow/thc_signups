# Imports
import calendar
from dataclasses import dataclass
from datetime import datetime, time, timedelta
from dateutil import tz
from dateutil.relativedelta import relativedelta


@dataclass
class RaidTime:
    day: int
    time: time

    @property
    def day_name(self):
        return calendar.day_name[self.day]


def _get_current_time_raid_tz(raid_tz: str) -> datetime:
    utc_now = datetime.now(tz.UTC)
    raid_tz_now = utc_now.astimezone(tz.gettz(raid_tz))
    return raid_tz_now


def get_raid_time_utc(raid_time: RaidTime, raid_tz: str) -> datetime:
    now = _get_current_time_raid_tz(raid_tz) + timedelta(days=1)
    raid_time = now + relativedelta(weekday=raid_time.day,
                                    hour=raid_time.time.hour,
                                    minute=raid_time.time.minute,
                                    second=0,
                                    microsecond=0)
    raid_time_utc = raid_time.astimezone(tz.UTC)
    return raid_time_utc

