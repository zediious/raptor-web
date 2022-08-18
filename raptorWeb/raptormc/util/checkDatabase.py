import logging

from raptormc.models import PlayerData, Server

def confirm_database_integrity():

    LOGGER = logging.getLogger(__name__)
    
    try:

        test_server = Server.objects.get(server_name="nomi")
        PlayerData.objects.get(server=test_server)
        
        LOGGER.error("[INFO] Tested for needed database objects, all good")

    except:
        
        LOGGER.error("[WARN] Needed database entries for playerCounts.py not present. Creating them now.")
        
        nomi = Server.objects.create(server_name="nomi")
        e6e = Server.objects.create(server_name="e6e")
        ct2 = Server.objects.create(server_name="ct2")
        ftbua = Server.objects.create(server_name="ftbua")
        ob = Server.objects.create(server_name="ob")
        hexxit = Server.objects.create(server_name="hexxit")
        network = Server.objects.create(server_name="network")

        nomi.save()
        e6e.save()
        ct2.save()
        ftbua.save()
        ob.save()
        hexxit.save()
        network.save()

        n_players = PlayerData.objects.create(server=nomi, player_count=0)
        e_players = PlayerData.objects.create(server=e6e, player_count=0)
        c_players = PlayerData.objects.create(server=ct2, player_count=0)
        f_players = PlayerData.objects.create(server=ftbua, player_count=0)
        o_players = PlayerData.objects.create(server=ob, player_count=0)
        h_players = PlayerData.objects.create(server=hexxit, player_count=0)
        total_players = PlayerData.objects.create(server=network, player_count=0)

        n_players.save()
        e_players.save()
        c_players.save()
        f_players.save()
        o_players.save()
        h_players.save()
        total_players.save()
