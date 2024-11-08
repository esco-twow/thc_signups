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
RAID_TIME_NA_BWL = time(20, 0)
RAID_TIME_EU_BWL = time(15, 0)
RAID_TIME_EU_STANDARD = time(14, 30)
RAID_TIME_PULL_TIME_MINUTES = 30

# Create raid commands define
# Note: The commands below contain special text identifiers to automatically create the SR links for raidres.fly.dev.
#       Docs for this are at https://raidres.fly.dev/raid-helper
#       These don't currently support HRs so you need to go and manually add those.
RAID_COMMAND_NA_MC = """
/quickcreate arguments:[template:02][title:Wednesday Weekly MC PUG][description:Bindings + mats HR. All others (eye, neck) open to SR. Non-class tier gear BOEs will be random rolled to the raid by the loot master (you don't need to roll - unless it is SR'ed).

We will start invites at the time noted for raid time, and start clearing ASAP. Clear time will depend on our DPS but average time is about 1 hour 15 minutes.

-MC -SR2 -DUP

][channel:#na-mc][date:{raid_discord_date}][time:{raid_discord_time}][advanced: <deletion: 12>]
"""

RAID_COMMAND_EU_MC = """
/quickcreate arguments:[template:02][title:Molten Core][description:Bindings, eye + mats HR. Neck open to SR. Non-class tier gear BOEs will be random rolled to the raid by the loot master (you don't need to roll - unless it is SR'ed).

We will start invites at the time noted for raid time, and start clearing ASAP. Clear time will depend on our DPS but average time is about 1 hour 15 minutes.

-MC -SR2 -DUP

][channel:#eu-monday-mc-pug][date:{raid_discord_date}][time:{raid_discord_time}][advanced: <deletion: 12>]
"""

RAID_COMMAND_EU_ES = """
/quickcreate arguments:[template:02][title:Emerald Sanctum][description:We do ES Hard Mode which means Erennius will **NOT** die. Do not SR loot that Erennius drops.

Legendary enchant HR for the guild.

-ES

][channel:#eu-es-signup][date:{raid_discord_date}][time:{raid_discord_time}][advanced: <deletion: 12>]
"""

RAID_COMMAND_NA_BWL = """
/quickcreate arguments:[template:02][title:Blackwing Lair][description:Mats HR. We will start invites at the time noted for raid time, and start clearing ASAP. Clear time will depend on our DPS.

-BWL -SR2 -DUP

][channel:#na-bwl-signup][date:{raid_discord_date}][time:{raid_discord_time}][advanced: <deletion: 12>]
"""

RAID_COMMAND_EU_BWL = """
/quickcreate arguments:[template:02][title:Blackwing Lair][description:This run will start right after our ES run ends; at approximately <t:{raid_utc_timestamp}:f>

**DFT, Nelth Tear, Rejuv Gem, and Styleen's have specific loot rules.** Read the pinned post in this channel for details!

-BWL -SR2 -DUP

][channel:#eu-bwl-signup][date:{raid_discord_date}][time:{raid_discord_time}][advanced: <deletion: 12>]
"""

RAID_COMMAND_EU_AQ40 = """
/quickcreate arguments:[template:02][title:Temple of Ahn'Qiraj][description:Please refer to the pinned post in this channel for additional **REQUIRED** consumes for this raid.

**For anyone hoping to soft reserve Bug Trio loot; we kill Vem last.** So please make sure you are NOT soft reserving loot that drops only when Princess Yauj or Lord Kri are killed last.

-AQ40 -SR2 -DUP

][channel:#eu-aq40-signup][date:{raid_discord_date}][time:{raid_discord_time}][advanced: <deletion: 12>]
"""

RAID_COMMAND_EU_NAXX_DAY1 = """
/quickcreate arguments:[template:02][title:Naxxramas Day 1][description:Please refer to the pinned post in this channel for additional **REQUIRED** consumes for this raid.

We will clear wings in the following order:
1. Abom Wing
2. DK Wing up to and including Gothik (Possibly 4hm - see note below)
3. Plague Wing
4. Spider Wing

**Four Horsemen - If we have the right composition with tanks & healers we will do it Day 1. We will decide before we start clearing and give a note and a moment to adjust SRs.**

Please soft reserve accordingly, as soft reserves from day 1 do **NOT** rollover into day 2, and soft reserves from day 2 do **NOT** apply to day 1; **NO EXCEPTIONS**.

-NAX -SR2 -DUP

][channel:#eu-naxx-day-1-signup][date:{raid_discord_date}][time:{raid_discord_time}][advanced: <deletion: 12>]
"""

RAID_COMMAND_EU_NAXX_DAY2 = """
/quickcreate arguments:[template:02][title:Naxxramas Day 2][description:Please refer to the pinned post in this channel for additional **REQUIRED** consumes for this raid.

On day 2 we will pickup wherever we left off on day 1 (if you didn't attend, don't hesitate to ask what we have left). Please place a soft reserve when signing up and revisit the soft reserve after day 1 is finished. Soft reserves from day 1 do **NOT** rollover into day 2, and soft reserves from day 2 do **NOT** apply to day 1; **NO EXCEPTIONS**.

-NAX

][channel:#eu-naxx-day-2-signup][date:{raid_discord_date}][time:{raid_discord_time}][advanced: <deletion: 12>]
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
    "eu_naxx_day1": Raid(day=calendar.SATURDAY, time=RAID_TIME_EU_STANDARD, command=RAID_COMMAND_EU_NAXX_DAY1),
    "eu_naxx_day2": Raid(day=calendar.SUNDAY, time=RAID_TIME_EU_STANDARD, command=RAID_COMMAND_EU_NAXX_DAY2),
    "eu_mc": Raid(day=calendar.MONDAY, time=RAID_TIME_EU_STANDARD, command=RAID_COMMAND_EU_MC),
}


# Post raid schedule define
RAID_SCHEDULE_TEXT = """
*The times posted below are **local to you** and are when we start the first pull; invites begin 30 minutes prior. Invites go out on a first come first serve basis (for Naxx/AQ40 we reserve the right to **choose** who we invite when we have an overabundance of signups). Don't be late!*

Our raid schedule for this week is:

{na_mc_day} <t:{na_mc_pull_time_timestamp}:f> - Molten Core (Hosted by USA boyz) <#1219397594862714930>

{na_bwl_day} <t:{na_bwl_pull_time_timestamp}:f> - BWL Molten Core (Hosted by USA boyz) <#1303912373630799922>

{eu_es_day} <t:{eu_es_timestamp}:f> - Emerald Sanctum Hard Mode <#1194352240023060521>
{eu_bwl_day} <t:{eu_bwl_timestamp}:f> - Black Wing Lair (Start time approximate; begins after ES) <#1194351759741694083> 

{eu_aq40_day} <t:{eu_aq40_timestamp}:f> - Temple of Ahn'Qiraj (Gear check required) <#1194351823323144202>

{eu_naxx_day1_day} <t:{eu_naxx_day1_timestamp}:f> - Naxxramas Day 1 (Gear check required) <#1207362552959344640>

{eu_naxx_day2_day} <t:{eu_naxx_day2_timestamp}:f> - Naxxramas Day 2 (Gear check required) <#1257103049261056050>

{eu_mc_day} <t:{eu_mc_timestamp}:f> - Molten Core (Hosted by guild) <#1191746258990276638>

*The times posted above are **local to you** and are when we start the first pull; invites begin 30 minutes prior. Invites go out on a first come first serve basis (for Naxx/AQ40 we reserve the right to **choose** who we invite when we have an overabundance of signups). Don't be late!*
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

