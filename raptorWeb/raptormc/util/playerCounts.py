from json import loads, dump
from requests import get

class PlayerCounts():
    """
    Object containing data structures and methods used for polling
    mcapi.us for information about Minecraft Servers.
    """ 
    # MCAPI request URLs for each server
    NOMI_ADDRESS = "https://mcapi.us/server/status?ip=nomi.shadowraptor.net";
    OB_ADDRESS = "https://mcapi.us/server/status?ip=ob.shadowraptor.net";
    FTBU_ADDRESS = "https://mcapi.us/server/status?ip=ftbu.shadowraptor.net";
    CT2_ADDRESS = "https://mcapi.us/server/status?ip=ct2.shadowraptor.net";
    E6E_ADDRESS = "https://mcapi.us/server/status?ip=e6e.shadowraptor.net";
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
        return str(ADDRESS.split(".")[1].split("=")[1])

    def request_info(self, ADDRESS, KEY):
        """
        Sets the "count", "names" and "online" keys within the provided "KEY" parameter
        to values gathered from an API request "ADDRESS" parameter.
        """
        if type(ADDRESS) == type("") and type(KEY) == type(""):

            serverJSON = loads(get(ADDRESS).text)

            if serverJSON["status"] != "error" and serverJSON["online"]:

                self.currentPlayers[KEY]["online"] = True
                
                self.currentPlayers[KEY]["count"] += serverJSON["players"]["now"]

                self.currentPlayers["totalCount"] += serverJSON["players"]["now"]

                for player in serverJSON["players"]["sample"]:

                    self.currentPlayers[KEY]["names"].append(player["name"])

        else:
            
            raise TypeError
        
        with open('playerCounts.LOCK', 'w') as lock_file:
            dump(serverJSON, lock_file)

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

        self.request_info(self.NOMI_ADDRESS, self.parse_key(self.NOMI_ADDRESS))
        self.request_info(self.FTBU_ADDRESS, self.parse_key(self.FTBU_ADDRESS))
        self.request_info(self.OB_ADDRESS, self.parse_key(self.OB_ADDRESS))
        self.request_info(self.CT2_ADDRESS, self.parse_key(self.CT2_ADDRESS))
        self.request_info(self.E6E_ADDRESS, self.parse_key(self.E6E_ADDRESS))

        return dict(self.currentPlayers)
