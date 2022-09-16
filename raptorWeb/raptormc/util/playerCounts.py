from mcstatus import JavaServer
from raptorWeb import settings
            
class PlayerCounts():
    """
    Object containing data structures and methods used for polling
    ShadowRaptor Minecraft servers for state and player information.
    """
    # Dictionary containing address/port/key names of servers
    SERVER_DATA = settings.SERVER_DATA
    # Dict to track player counts and names in each server internally
    currentPlayers = {}
    # Template context dictionary
    currentPlayers_DB = {}     

    def parse_key (self, ADDRESS):
        """
        Returns a string that represents a key in the "currentPlayers" 
        Dictionary, gathered from domain name "ADDRESS" parameter.
        """
        return str(ADDRESS.split(".")[0])

    def request_info(self, ADDRESS, PORT, KEY):
        """
        Sets the "count", "names" and "online" keys within the provided "KEY" parameter
        to values gathered from a domain name "ADDRESS" parameter.
        """
        if type(ADDRESS) == type("") and type(KEY) == type(""):

            try:

                serverJSON = JavaServer(ADDRESS, PORT).query()

                self.currentPlayers[KEY]["online"] = True
            
                self.currentPlayers[KEY]["count"] += serverJSON.players.online

                self.currentPlayers["totalCount"] += serverJSON.players.online

                for player in serverJSON.players.names:

                    self.currentPlayers[KEY]["names"].append(player)

            except TimeoutError:

                pass

        else:
            
            raise TypeError

    def get_current_players(self):
        """
        Return a dictionary containing total player count, as well as nested dictionaries
        with specific counts, player names and states for each server
        """
        self.currentPlayers = {
            "totalCount": 0,
            "nomi": {
                "count": 0,
                "names": [],
                "online": False
            },
            "ob": {
                "count": 0,
                "names": [],
                "online": False
            },
            "ftbu": {
                "count": 0,
                "names": [],
                "online": False
            },
            "ct2": {
                "count": 0,
                "names": [],
                "online": False
            },
            "e6e": {
                "count": 0,
                "names": [],
                "online": False
            }

        }

        for server in self.SERVER_DATA:

            self.request_info(
                self.SERVER_DATA[server]["address"], 
                self.SERVER_DATA[server]["port"], 
                self.parse_key(self.SERVER_DATA[server]["address"]))

        with open('playerCounts.LOCK', 'w') as lock_file:
            lock_file.write("playerCounts.PY LOCK File. Do not modify manually.")

        return dict(self.currentPlayers)
