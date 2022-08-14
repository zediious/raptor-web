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

            def parse_key (ADDRESS):
                """
                Returns a string that represents a key in the "currentPlayers" 
                Dictionary, gathered from API request "ADDRESS" parameter.
                """
                return str(ADDRESS.split(".")[1].split("=")[1])

            def request_info(ADDRESS, KEY):
                """
                Sets the "count" and "names" keys within the provided "KEY" parameter
                to values gathered from an API request "ADDRESS" parameter. The "count" key
                is an integer, the "names" key is a List of strings.
                """

                currentPlayers = ShadowRaptor.Tool.PlayerCounts.currentPlayers

                if type(ADDRESS) == type("") and type(KEY) == type(""):

                    serverJSON = json.loads(requests.get(ADDRESS).text)

                    if serverJSON["status"] != "error" and serverJSON["online"]:

                        currentPlayers[KEY]["count"] += serverJSON["players"]["now"]

                        currentPlayers["totalCount"] += serverJSON["players"]["now"]

                        for player in serverJSON["players"]["sample"]:

                            currentPlayers[KEY]["names"].append(player["name"])

                    else:

                        pass

                else:
                    
                    raise TypeError

            def get_current_players():
                """
                Return a dictionary containing total player count, as well as nested dictionaries
                with specific counts and player names for each server
                """
                SR = ShadowRaptor.Tool.PlayerCounts
                
                SR.request_info(SR.NOMI_ADDRESS, SR.parse_key(SR.NOMI_ADDRESS))
                SR.request_info(SR.FTBU_ADDRESS, SR.parse_key(SR.FTBU_ADDRESS))
                SR.request_info(SR.OB_ADDRESS, SR.parse_key(SR.OB_ADDRESS))
                SR.request_info(SR.CT2_ADDRESS, SR.parse_key(SR.CT2_ADDRESS))
                SR.request_info(SR.E6E_ADDRESS, SR.parse_key(SR.E6E_ADDRESS))

                return dict(SR.currentPlayers)

            def get_total_count(self):
                """
                Return the integer of "totalCount" key from currentPlayers dict, after returning get_current_players() internally
                """
                ShadowRaptor.Tool.PlayerCounts.currentPlayers["totalCount"] = 0

                dict = ShadowRaptor.Tool.PlayerCounts.get_current_players()
                return int(dict["totalCount"])

