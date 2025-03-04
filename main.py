# Imports
import calendar
from datetime import time, timedelta
from dateutil import tz
from helpers import get_raid_time_utc, get_next_raid_week_reset_date, Raid
from typing import Dict


# The discord raid create bot wants the times in EST, so if that ever changes, adjust this accordingly.
RAID_DISCORD_TZ = "US/Eastern"

# A few time defines in case standard raid time changes
# Note: The times are in CST timezone (cause that's where I live, so it's easiest for me). They are in 24-hour format
#       and don't need to be adjusted for daylight savings, unless you want to change the raid time based on CST. If you
#       want to do it in a different timezone, change RAID_TIME_TZ and adjust the time() values accordingly.
RAID_TZ = "US/Central"
RAID_WEEK_RESET_WEEKDAY = calendar.TUESDAY
RAID_TIME_NA_MC = time(19, 0)
RAID_TIME_NA_BWL = time(19, 0)
RAID_TIME_EU_BWL = time(15, 0)
RAID_TIME_EU_STANDARD = time(14, 30)
RAID_TIME_PULL_TIME_MINUTES = 30

# Create raid commands define
# Note: The commands below contain special text identifiers to automatically create the SR links for raidres.fly.dev.
#       Docs for this are at https://raidres.fly.dev/raid-helper
#       These don't currently support HRs so you need to go and manually add those.
RAID_COMMAND_NA_MC = """
/quickcreate arguments:[template:2][title:NA Weekly MC PUG][description:Garr bindings + mats HR. All others (Geddon binding, eye, neck, mount) open to SR. Non-class tier gear BOEs will be random rolled to the raid by the loot master (you don't need to roll - unless it is SR'ed).

Geddon binding SR will be given preference to those who already have Garr binding or at least some/most TF mats.

We will start invites at the time noted for raid time, and start clearing ASAP. Clear time will depend on our DPS but average time is about 1 hour 15 minutes.

-MC -SR2 -DUP

][channel:#na-mc-signup][date:{raid_discord_date}][time:{raid_discord_time}][advanced: <deletion: 12>]
"""

RAID_COMMAND_EU_MC = """
/quickcreate arguments:[template:2][title:Molten Core][description:Bindings, eye + mats HR. Neck, mount open to SR. Non-class tier gear BOEs will be random rolled to the raid by the loot master (you don't need to roll - unless it is SR'ed).

We will start invites at the time noted for raid time, and start clearing ASAP. Clear time will depend on our DPS but average time is about 1 hour 15 minutes.

-MC -SR2 -DUP

][channel:#eu-monday-mc-pug][date:{raid_discord_date}][time:{raid_discord_time}][advanced: <deletion: 12>]
"""

RAID_COMMAND_EU_ES = """
/quickcreate arguments:[template:2][title:Emerald Sanctum][description:We do ES Hard Mode which means Erennius will **NOT** die. Do not SR loot that Erennius drops.

Legendary enchant HR for the guild.

-ES

][channel:#eu-es-signup][date:{raid_discord_date}][time:{raid_discord_time}][advanced: <deletion: 12>]
"""

RAID_COMMAND_NA_BWL = """
/quickcreate arguments:[template:2][title:NA Weekly BWL PUG][description:Mats HR. We will start invites at the time noted for raid time, and start clearing ASAP. Clear time will depend on our DPS.

-BWL -SR2 -DUP

][channel:#na-bwl-signup][date:{raid_discord_date}][time:{raid_discord_time}][advanced: <deletion: 12>]
"""

RAID_COMMAND_EU_BWL = """
/quickcreate arguments:[template:2][title:Blackwing Lair][description:This run will start right after our ES run ends; at approximately <t:{raid_utc_timestamp}:f>

**DFT and Styleen's have specific loot rules.** Read the pinned post in this channel for details!

-BWL -SR2 -DUP

][channel:#eu-bwl-signup][date:{raid_discord_date}][time:{raid_discord_time}][advanced: <deletion: 12>]
"""

RAID_COMMAND_EU_AQ40 = """
/quickcreate arguments:[template:2][title:Temple of Ahn'Qiraj][description:Please refer to the pinned post in this channel for additional **REQUIRED** consumes for this raid.

**For anyone hoping to soft reserve Bug Trio loot; we kill Yauj last.** So please make sure you are NOT soft reserving loot that drops only when Vem or Lord Kri are killed last.

-AQ40 -SR2 -DUP

][channel:#eu-aq40-signup][date:{raid_discord_date}][time:{raid_discord_time}][advanced: <deletion: 12>]
"""

RAID_COMMAND_EU_NAXX = """
/quickcreate arguments:[template:2][title:Naxxramas][description:Please refer to the pinned post in this channel for additional **REQUIRED** consumes for this raid.

**In preparation for Kara40 schedule, we are extending the time for Naxx and will be doing a single day full clear of Naxx.**

We will clear wings in the following order:
1. Abom Wing
2. DK Wing (including 4hm)
3. Plague Wing
4. Spider Wing
5. Upper - Saph & KT

-NAX -SR2 -DUP

][channel:#eu-naxx-day-1-signup][date:{raid_discord_date}][time:{raid_discord_time}][advanced: <deletion: 12>]
"""

# Raid defines
# Note: The times are in CST timezone (cause that's where I live, so it's easiest for me). They are in 24-hour format
#       and don't need to be adjusted for daylight savings, unless you want to change the raid time based on CST. If you
#       want to do it in a different timezone, change RAID_TIME_TZ and adjust the time() values accordingly.
RAIDS: Dict[str, Raid]
RAIDS = {
    "na_mc": Raid(day=calendar.WEDNESDAY, time=RAID_TIME_NA_MC, command=RAID_COMMAND_NA_MC),
    "na_bwl": Raid(day=calendar.THURSDAY, time=RAID_TIME_NA_BWL, command=RAID_COMMAND_NA_BWL),
    "eu_es": Raid(day=calendar.THURSDAY, time=RAID_TIME_EU_STANDARD, command=RAID_COMMAND_EU_ES),
    "eu_bwl": Raid(day=calendar.THURSDAY, time=RAID_TIME_EU_BWL, command=RAID_COMMAND_EU_BWL),
    "eu_aq40": Raid(day=calendar.FRIDAY, time=RAID_TIME_EU_STANDARD, command=RAID_COMMAND_EU_AQ40),
    "eu_naxx": Raid(day=calendar.SATURDAY, time=RAID_TIME_EU_STANDARD, command=RAID_COMMAND_EU_NAXX),
    "eu_mc": Raid(day=calendar.MONDAY, time=RAID_TIME_EU_STANDARD, command=RAID_COMMAND_EU_MC),
}

# Post raid schedule define
# Note: Each key from RAIDS define above will get three variables added for each key that can be used in the
#       RAID_SCHEDULE_TEXT define below:
#       <key>_day - this is the day of the raid (e.g. Wednesday)
#       <key>_timestamp - this is the UCT timestamp of the raid as an integer value
#       <key>_pull_time_timestamp - this is the pull time timestamp of the raid as an integer value (only used for NA
#                                   MC & BWL)
#
#       For example if there is a key "na_mc" in RAIDS, you will get the following available variables:
#       na_mc_day
#       na_mc_timestamp
#       na_mc_pull_time_timestamp
RAID_SCHEDULE_TEXT = """
Our raid schedule for this week is:

{na_mc_day} <t:{na_mc_pull_time_timestamp}:f> - Molten Core (Hosted by USA boyz) <#1219397594862714930>

{na_bwl_day} <t:{na_bwl_pull_time_timestamp}:f> - BWL (Hosted by USA boyz) <#1303912373630799922>

{eu_es_day} <t:{eu_es_timestamp}:f> - Emerald Sanctum Hard Mode <#1194352240023060521>
{eu_bwl_day} <t:{eu_bwl_timestamp}:f> - Black Wing Lair (Start time approximate; begins after ES) <#1194351759741694083> 

{eu_aq40_day} <t:{eu_aq40_timestamp}:f> - Temple of Ahn'Qiraj (Gear check required) <#1194351823323144202>

{eu_naxx_day} <t:{eu_naxx_timestamp}:f> - Naxxramas (Gear check required) <#1207362552959344640>

{eu_mc_day} <t:{eu_mc_timestamp}:f> - Molten Core (Hosted by guild) <#1191746258990276638>

The times posted above are **local to you** and are when we start the first pull (unless noted); invites begin 30 minutes prior. For most raids, invites go out on a first come first serve basis. For Naxx, we will prioritize invites based on raid composition when we have an overabundance of signups. **Don't be late!**
"""


def main():
    post_keys = {}

    next_raid_week_reset_date = get_next_raid_week_reset_date(RAID_TZ, RAID_WEEK_RESET_WEEKDAY)

    for key, raid in RAIDS.items():
        raid_time_utc = get_raid_time_utc(raid, next_raid_week_reset_date)
        raid_time_pull_time_utc = raid_time_utc + timedelta(minutes=RAID_TIME_PULL_TIME_MINUTES)
        post_keys[f"{key}_timestamp"] = str(int(raid_time_utc.timestamp()))
        post_keys[f"{key}_pull_time_timestamp"] = str(int(raid_time_pull_time_utc.timestamp()))
        post_keys[f"{key}_day"] = raid.day_name
        raid_utc_timestamp = str(int(raid_time_utc.timestamp()))
        raid_discord_datetime = raid_time_utc.astimezone(tz.gettz(RAID_DISCORD_TZ))
        raid_discord_date = raid_discord_datetime.strftime("%Y-%m-%d")
        raid_discord_time = raid_discord_datetime.strftime("%H:%M")
        command_text = raid.command.format(
            raid_discord_date=raid_discord_date,
            raid_discord_time=raid_discord_time,
            raid_utc_timestamp=raid_utc_timestamp,
        )
        print(f'{key} Create Raid Command')
        print('-------------------------------------------------------------------------------------------------------')
        print(command_text)
        print('')
        print('')

    raid_schedule_text = RAID_SCHEDULE_TEXT.format(**post_keys)
    print('RAID SCHEDULE')
    print('-----------------------------------------------------------------------------------------------------------')
    print(raid_schedule_text)
    print('')
    print('')


if __name__ == "__main__":
    main()

