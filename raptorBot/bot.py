import os
import discord
from dotenv import load_dotenv
from json import dumps

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

ANNOUNCEMENT_CHANNEL = 741015006480564254

class RaptorClient(discord.Client):

    async def on_ready(self):
        """
        Triggers when the bot has logged in and is ready.
        """
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        """
        Triggers when a message is sent in the Discord Server.
        Gets all messages from the "Announcements" Channel and
        places their content in a Dictionary, nested in another
        dictionary keyed by a counteryed number. The nested 
        dictionary containing the message is keyed by the author.
        Data is saved to an announcements.json each iteration.
        """
        channel = client.get_channel(ANNOUNCEMENT_CHANNEL)
        if message.channel == channel:

            messages = [message async for message in channel.history(limit=5)]
            announcements = {}

            key = 0
            for message in messages:
                announcements.update({
                    "message{}".format(key): {
                        "author": str(message.author),
                        "message": message.content
                        }
                })
                key += 1

            announcementsJSON = open("../raptorWeb/announcements.json", "w")
            announcementsJSON.write(dumps(announcements, indent=4))
            announcementsJSON.close()

intents = discord.Intents.all()
intents.message_content = True

client = RaptorClient(intents=intents)
client.run(TOKEN)
