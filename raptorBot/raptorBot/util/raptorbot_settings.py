from os import getenv
from dotenv import load_dotenv

# Load .env file and load Bot Token from file
load_dotenv()
TOKEN = getenv('DISCORD_TOKEN')

# Settings for the Discord Bot
DESCRIPTION = "I do work for the ShadowRaptorMC website!"
DISCORD_GUILD = 740388741079760937
ANNOUNCEMENT_CHANNEL_ID = 741015006480564254
SERVER_ANNOUNCEMENT_CHANNEL_IDS = {
    "ob": 897710478678163526,
    "ftbu": 916808914828423168,
    "ct2": 937592813393162280,
    "e6e": 956730958013411358,
    "nomi": 990473836606677023,
    "atm7": 1024894719886631003

}
STAFF_ROLE_ID = 937891209291120660
