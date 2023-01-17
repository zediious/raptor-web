from mcstatus import JavaServer
            
class PlayerCounts():
    """
    Object containing data structures and methods used for polling
    ShadowRaptor Minecraft servers for state and player information.
    """
    # Dictionary containing address/port/key names of servers
    server_data = {}
    # Dict to track player counts and names in each server internally
    currentPlayers = {}
    # Template context dictionary
    currentPlayers_DB = {
        "server_info": [],
        "totalCount": 0
    }     

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
                self.currentPlayers["totalCount"] += serverJSON.players.online
                self.currentPlayers.update({
                    KEY: {
                        "address": ADDRESS,
                        "online": True,
                        "count": serverJSON.players.online,
                        "names": [player for player in serverJSON.players.names]
                    }
                })

            except TimeoutError:
                self.currentPlayers.update({
                    KEY: {
                        "address": ADDRESS,
                        "online": False,
                        "count": 0,
                        "names": []
                    }
                })

        else:
            raise TypeError

    def get_current_players(self):
        """
        Return a dictionary containing total player count, as well as nested dictionaries
        with specific counts, player names and states for each server
        """
        self.currentPlayers = {
            "totalCount": 0
        }

        for server in self.server_data:

            self.request_info(
                self.server_data[server]["address"], 
                self.server_data[server]["port"], 
                self.parse_key(self.server_data[server]["address"]))

        with open('playerCounts.LOCK', 'w') as lock_file:
            lock_file.write("playerCounts.PY LOCK File. Do not modify manually.")

        return dict(self.currentPlayers)
