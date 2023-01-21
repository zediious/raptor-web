from os import getenv
from dotenv import load_dotenv

# Load .env file and load Bot Token from file
load_dotenv()
TOKEN = getenv('DISCORD_TOKEN')

# Settings for the Discord Bot
DESCRIPTION = "I do work for the ShadowRaptorMC website!"
DISCORD_GUILD = 740388741079760937
ANNOUNCEMENT_CHANNEL_ID = 741015006480564254
STAFF_ROLE_ID = 937891209291120660
