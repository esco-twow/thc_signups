# Imports
import calendar
from datetime import time
from dateutil import tz
from helpers import get_raid_time_utc, RaidTime
from typing import Dict


# SR link defines
# I split these out separately and added them at the top here to make my life easier because they are what change
#  most frequently.
# The keys here need to match the keys in RAIDS define.
SR_LINKS = {
    "mc_na": "",
    "es": "",
    "bwl": "",
    "aq40": "",
    "naxx_day1": "",
    "naxx_day2": "",
    "mc_eu": "",
}

# The discord raid create bot wants the times in EST, so if that ever changes, adjust this accordingly.
RAID_DISCORD_TZ = "US/Eastern"

# A few time defines in case standard raid time changes
# Note: The times are in CST timezone (cause that's where I live, so it's easiest for me). They are in 24-hour format
#       and don't need to be adjusted for daylight savings, unless you want to change the raid time based on CST. If you
#       want to do it in a different timezone, change RAID_TIME_TZ and adjust the time() values accordingly.
RAID_TZ = "US/Central"
RAID_TIME_MC_NA = time(19, 0)
RAID_TIME_BWL = time(15, 0)
RAID_TIME_STANDARD_EU = time(14, 30)

# Raid defines
# Note: The times are in CST timezone (cause that's where I live, so it's easiest for me). They are in 24-hour format
#       and don't need to be adjusted for daylight savings, unless you want to change the raid time based on CST. If you
#       want to do it in a different timezone, change RAID_TIME_TZ and adjust the time() values accordingly.
RAIDS: Dict[str, RaidTime]
RAIDS = {
    "mc_na": RaidTime(day=calendar.WEDNESDAY, time=RAID_TIME_MC_NA),
    "es": RaidTime(day=calendar.THURSDAY, time=RAID_TIME_STANDARD_EU),
    "bwl": RaidTime(day=calendar.THURSDAY, time=RAID_TIME_BWL),
    "aq40": RaidTime(day=calendar.FRIDAY, time=RAID_TIME_STANDARD_EU),
    "naxx_day1": RaidTime(day=calendar.SATURDAY, time=RAID_TIME_STANDARD_EU),
    "naxx_day2": RaidTime(day=calendar.SUNDAY, time=RAID_TIME_STANDARD_EU),
    "mc_eu": RaidTime(day=calendar.MONDAY, time=RAID_TIME_STANDARD_EU),
}

# Create raid commands define
RAID_COMMAND_MC_NA = """
/quickcreate arguments:[template:02][title:Wednesday Weekly MC PUG][description:Bindings + mats HR. All others (eye, neck) open to SR. Non-class tier gear BOEs will be random rolled to the raid by the loot master (you don't need to roll - unless it is SR'ed).

We will start invites at the time noted for raid time, and start clearing ASAP. Clear time will depend on our DPS but average time is about 1 hour 15 minutes.

{sr_link}][channel:#wednesday-mc-pug][date:{raid_discord_date}][time:{raid_discord_time}]
"""

RAID_COMMAND_MC_EU = """
/quickcreate arguments:[template:02][title:Molten Core][description:Bindings + mats HR. All others (eye, neck) open to SR. Non-class tier gear BOEs will be random rolled to the raid by the loot master (you don't need to roll - unless it is SR'ed).

We will start invites at the time noted for raid time, and start clearing ASAP. Clear time will depend on our DPS but average time is about 1 hour 15 minutes.

{sr_link}][channel:#monday-mc-pug][date:{raid_discord_date}][time:{raid_discord_time}]
"""

RAID_COMMAND_ES = """
/quickcreate arguments:[template:02][title:Emerald Sanctum][description:We do ES Hard Mode which means Erennius will **NOT** die. Do not SR loot that Erennius drops.

Legendary enchant HR for the guild.

{sr_link}][channel:#es-signup][date:{raid_discord_date}][time:{raid_discord_time}]
"""

RAID_COMMAND_BWL = """
/quickcreate arguments:[template:02][title:Blackwing Lair][description:This run will start right after our ES run ends; at approximately <t:{raid_utc_timestamp}:f>

**DFT, Nelth Tear, and Rejuv Gem have specific loot rules.** Read the pinned post in this channel for details!

{sr_link}][channel:#bwl-signup][date:{raid_discord_date}][time:{raid_discord_time}]
"""

RAID_COMMAND_AQ40 = """
/quickcreate arguments:[template:02][title:Temple of Ahn'Qiraj][description:Please refer to the pinned post in this channel for additional **REQUIRED** consumes for this raid.

**For anyone hoping to soft reserve Bug Trio loot; we kill Vem last.** So please make sure you are NOT soft reserving loot that drops only when Princess Yauj or Lord Kri are killed last.

{sr_link}][channel:#aq40-signup][date:{raid_discord_date}][time:{raid_discord_time}]
"""

RAID_COMMAND_NAXX_DAY1 = """
/quickcreate arguments:[template:02][title:Naxxramas Day 1][description:Please refer to the pinned post in this channel for additional **REQUIRED** consumes for this raid.

We will clear wings in the following order:
1. Abom Wing
2. DK Wing up to and including Gothik (Possibly 4hm - see note below)
3. Plague Wing
4. Spider Wing

**Four Horsemen - If we have the right composition with tanks & healers we will do it Day 1. We will decide before we start clearing and give a note and a moment to adjust SRs.**

Please soft reserve accordingly, as soft reserves from day 1 do **NOT** rollover into day 2, and soft reserves from day 2 do **NOT** apply to day 1; **NO EXCEPTIONS**.

{sr_link}][channel:#naxx-day-1-signup][date:{raid_discord_date}][time:{raid_discord_time}]
"""

RAID_COMMAND_NAXX_DAY2 = """
/quickcreate arguments:[template:02][title:Naxxramas Day 2][description:Please refer to the pinned post in this channel for additional **REQUIRED** consumes for this raid.

On day 2 we will pickup wherever we left off on day 1 (if you didn't attend, don't hesitate to ask what we have left). Please place a soft reserve when signing up and revisit the soft reserve after day 1 is finished. Soft reserves from day 1 do **NOT** rollover into day 2, and soft reserves from day 2 do **NOT** apply to day 1; **NO EXCEPTIONS**.

{sr_link}][channel:#naxx-day-2-signup][date:{raid_discord_date}][time:{raid_discord_time}]
"""

RAID_COMMANDS = {
    "mc_na": RAID_COMMAND_MC_NA,
    "es": RAID_COMMAND_ES,
    "bwl": RAID_COMMAND_BWL,
    "aq40": RAID_COMMAND_AQ40,
    "naxx_day1": RAID_COMMAND_NAXX_DAY1,
    "naxx_day2": RAID_COMMAND_NAXX_DAY2,
    "mc_eu": RAID_COMMAND_MC_EU,
}

# Post raid schedule define
RAID_SCHEDULE_TEXT = """
*The times posted below are **local to you** and are when we start the first pull; invites begin 30 minutes prior. Invites go out on a first come first serve basis (for Naxx/AQ40 we reserve the right to **choose** who we invite when we have an overabundance of signups). Don't be late!*

Our raid schedule for this week is:

{mc_na_day} <t:{mc_na_timestamp}:f> - Molten Core (Hosted by USA boyz) <#1219397594862714930>

{es_day} <t:{es_timestamp}:f> - Emerald Sanctum Hard Mode <#1194352240023060521>
{bwl_day} <t:{bwl_timestamp}:f> - Black Wing Lair (Start time approximate; begins after ES) <#1194351759741694083> 

{aq40_day} <t:{aq40_timestamp}:f> - Temple of Ahn'Qiraj (Gear check required) <#1194351823323144202>

{naxx_day1_day} <t:{naxx_day1_timestamp}:f> - Naxxramas Day 1 (Gear check required) <#1207362552959344640>

{naxx_day2_day} <t:{naxx_day2_timestamp}:f> - Naxxramas Day 2 (Gear check required) <#1257103049261056050>

{mc_eu_day} <t:{mc_eu_timestamp}:f> - Molten Core (Hosted by guild) <#1191746258990276638>

*The times posted above are **local to you** and are when we start the first pull; invites begin 30 minutes prior. Invites go out on a first come first serve basis (for Naxx/AQ40 we reserve the right to **choose** who we invite when we have an overabundance of signups). Don't be late!*
"""


def main():
    raid_times = {}
    post_keys = {}
    for key, raid_time in RAIDS.items():
        raid_time_utc = get_raid_time_utc(raid_time, RAID_TZ)
        post_keys[f"{key}_timestamp"] = str(int(raid_time_utc.timestamp()))
        post_keys[f"{key}_day"] = raid_time.day_name
        raid_times[key] = raid_time_utc

    for key, command in RAID_COMMANDS.items():
        sr_link = SR_LINKS[key]
        raid_time_utc = raid_times[key]
        raid_utc_timestamp = str(int(raid_time_utc.timestamp()))
        raid_discord_datetime = raid_time_utc.astimezone(tz.gettz(RAID_DISCORD_TZ))
        raid_discord_date = raid_discord_datetime.strftime("%Y-%m-%d")
        raid_discord_time = raid_discord_datetime.strftime("%H:%M")
        command_text = command.format(
            sr_link=sr_link,
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

