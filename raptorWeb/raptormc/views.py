from django.shortcuts import render
from django.http import HttpResponse
from raptorWeb import settings

from os.path import join
import json
import requests

# Create your views here.

TEMPLATE_DIR_RAPTORMC = join(settings.TEMPLATE_DIR, "raptormc")

class ShadowRaptor():

    class Info():

        async def home_servers(request):
            
            # player_getter = ShadowRaptor.Tool.PlayerCounts()
            
            # home_servers_data = {"player_count": player_getter.get_total_count()}
            # return render(request, join(TEMPLATE_DIR_RAPTORMC, "home.html"), context = home_servers_data)

            home_servers_data = {"player_count": 7}
            return render(request, join(TEMPLATE_DIR_RAPTORMC, "home.html"), context = home_servers_data)
        
        def rules(request):

            return HttpResponse("Rules")
            
        def banned_items(request):

            return HttpResponse("Banned Items")

    class Tool():

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

                    serverJSON = json.loads(requests.get(ADDRESS).text)

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
                
                self.request_info(self.NOMI_ADDRESS, self.parse_key(self.NOMI_ADDRESS))
                self.request_info(self.FTBU_ADDRESS, self.parse_key(self.FTBU_ADDRESS))
                self.request_info(self.OB_ADDRESS, self.parse_key(self.OB_ADDRESS))
                self.request_info(self.CT2_ADDRESS, self.parse_key(self.CT2_ADDRESS))
                self.request_info(self.E6E_ADDRESS, self.parse_key(self.E6E_ADDRESS))

                return dict(self.currentPlayers)

            def get_total_count(self):
                """
                Return the integer of "totalCount" key from currentPlayers dict, after returning get_current_players() internally
                """
                self.currentPlayers["totalCount"] = 0
                self.get_current_players()

                return int(self.currentPlayers["totalCount"])

