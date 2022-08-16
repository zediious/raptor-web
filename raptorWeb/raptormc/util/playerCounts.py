from json import loads
from requests import get


class PlayerCounts():
            
    # MCAPI request URLs for each server
    NOMI_ADDRESS = "https://mcapi.us/server/status?ip=nomi.shadowraptor.net";
    OB_ADDRESS = "https://mcapi.us/server/status?ip=ob.shadowraptor.net";
    FTBU_ADDRESS = "https://mcapi.us/server/status?ip=ftbu.shadowraptor.net";
    CT2_ADDRESS = "https://mcapi.us/server/status?ip=ct2.shadowraptor.net";
    E6E_ADDRESS = "https://mcapi.us/server/status?ip=e6e.shadowraptor.net";

    # Dict to track player counts and names in each server
    currentPlayers = {
        "totalCount": 0,
        "nomi": {
            "count": 0,
            "names": []
        },
        "ob": {
            "count": 0,
            "names": []
        },
        "ftbu": {
            "count": 0,
            "names": []
        },
        "ct2": {
            "count": 0,
            "names": []
        },
        "e6e": {
            "count": 0,
            "names": []
        }

    }            

    def parse_key (self, ADDRESS):
        """
        Returns a string that represents a key in the "currentPlayers" 
        Dictionary, gathered from API request "ADDRESS" parameter.
        """
        return str(ADDRESS.split(".")[1].split("=")[1])

    def request_info(self, ADDRESS, KEY):
        """
        Sets the "count" and "names" keys within the provided "KEY" parameter
        to values gathered from an API request "ADDRESS" parameter. The "count" key
        is an integer, the "names" key is a List of strings.
        """
        if type(ADDRESS) == type("") and type(KEY) == type(""):

            serverJSON = loads(get(ADDRESS).text)

            if serverJSON["status"] != "error" and serverJSON["online"]:

                self.currentPlayers[KEY]["count"] += serverJSON["players"]["now"]

                self.currentPlayers["totalCount"] += serverJSON["players"]["now"]

                for player in serverJSON["players"]["sample"]:

                    self.currentPlayers[KEY]["names"].append(player["name"])

            else:

                pass

        else:
            
            raise TypeError

    def get_current_players(self):
        """
        Return a dictionary containing total player count, as well as nested dictionaries
        with specific counts and player names for each server
        """
        self.currentPlayers = {
            "totalCount": 0,
            "nomi": {
                "count": 0,
                "names": []
            },
            "ob": {
                "count": 0,
                "names": []
            },
            "ftbu": {
                "count": 0,
                "names": []
            },
            "ct2": {
                "count": 0,
                "names": []
            },
            "e6e": {
                "count": 0,
                "names": []
            }

        }

        self.request_info(self.NOMI_ADDRESS, self.parse_key(self.NOMI_ADDRESS))
        self.request_info(self.FTBU_ADDRESS, self.parse_key(self.FTBU_ADDRESS))
        self.request_info(self.OB_ADDRESS, self.parse_key(self.OB_ADDRESS))
        self.request_info(self.CT2_ADDRESS, self.parse_key(self.CT2_ADDRESS))
        self.request_info(self.E6E_ADDRESS, self.parse_key(self.E6E_ADDRESS))

        return dict(self.currentPlayers)

    def get_total_count(self):
        """
        Return the integer of "totalCount" key from currentPlayers dict
        """
        return int(self.currentPlayers["totalCount"])
