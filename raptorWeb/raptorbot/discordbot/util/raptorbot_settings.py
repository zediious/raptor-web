from os import getenv
from dotenv import load_dotenv

# Load .env file and load Bot Token from file
load_dotenv()
TOKEN = getenv('DISCORD_TOKEN')

# Settings for the Discord Bot
DESCRIPTION = "I do work for the ShadowRaptorMC website!"
DISCORD_GUILD = int(getenv('DISCORD_GUILD'))
ANNOUNCEMENT_CHANNEL_ID = int(getenv('ANNOUNCEMENT_CHANNEL_ID'))
STAFF_ROLE_ID = int(getenv('STAFF_ROLE_ID'))
