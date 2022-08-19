from multiprocessing import connection
from sqlite3 import Time
from mcstatus import JavaServer
            
class PlayerCounts():
    """
    Object containing data structures and methods used for polling
    mcapi.us for information about Minecraft Servers.
    """ 
    # Domain names for servers
    NOMI_ADDRESS = "nomi.shadowraptor.net"
    OB_ADDRESS = "ob.shadowraptor.net"
    FTBU_ADDRESS = "ftbu.shadowraptor.net"
    CT2_ADDRESS = "ct2.shadowraptor.net"
    E6E_ADDRESS = "e6e.shadowraptor.net"
    # Dict to track player counts and names in each server internally
    currentPlayers = {
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
    # Template Variable Dictionary
    currentPlayers_DB = {"player_count": 0,
                        "nomi_names": "",
                        "nomi_state": False,
                        "e6e_names": "e6eNames",
                        "e6e_state": False,
                        "ct2_names": "ct2Names",
                        "ct2_state": False,
                        "ftbu_names": "ftbuNames",
                        "ftbu_state": False,
                        "ob_names": "obNames",
                        "ob_state": False,
                        "hexxit_names": "hexxitNames",
                        "hexxit_state": False}     

    def parse_key (self, ADDRESS):
        """
        Returns a string that represents a key in the "currentPlayers" 
        Dictionary, gathered from API request "ADDRESS" parameter.
        """
        return str(ADDRESS.split(".")[0])

    def request_info(self, ADDRESS, PORT, KEY):
        """
        Sets the "count", "names" and "online" keys within the provided "KEY" parameter
        to values gathered from an API request "ADDRESS" parameter.
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

        self.request_info(self.NOMI_ADDRESS, 25566, self.parse_key(self.NOMI_ADDRESS))
        self.request_info(self.FTBU_ADDRESS, 25568, self.parse_key(self.FTBU_ADDRESS))
        self.request_info(self.OB_ADDRESS, 25567, self.parse_key(self.OB_ADDRESS))
        self.request_info(self.CT2_ADDRESS, 25569, self.parse_key(self.CT2_ADDRESS))
        self.request_info(self.E6E_ADDRESS, 25570, self.parse_key(self.E6E_ADDRESS))

        with open('playerCounts.LOCK', 'w') as lock_file:
            lock_file.write("playerCounts.PY LOCK File. Do not modify manually.")

        return dict(self.currentPlayers)
