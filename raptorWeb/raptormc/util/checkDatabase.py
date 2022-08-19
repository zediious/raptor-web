import logging

from raptormc.models import Server

def confirm_database_integrity():
    """
    Checks that Server objects exist. If not, they will be created.
    """
    LOGGER = logging.getLogger(__name__)
    
    try:

        Server.objects.get(server_name="nomi")
        Server.objects.get(server_name="e6e")
        Server.objects.get(server_name="ct2")
        Server.objects.get(server_name="ftbu")
        Server.objects.get(server_name="ob")
        Server.objects.get(server_name="hexxit")
        Server.objects.get(server_name="network")
        
        LOGGER.error("[INFO] Tested for needed database objects, all good")

    except:
        
        LOGGER.error("[WARN] Needed database entries for playerCounts.py not present. Creating them now.")

        Server.objects.all().delete()
        
        nomi = Server.objects.create(server_name="nomi")
        e6e = Server.objects.create(server_name="e6e")
        ct2 = Server.objects.create(server_name="ct2")
        ftbu = Server.objects.create(server_name="ftbu")
        ob = Server.objects.create(server_name="ob")
        hexxit = Server.objects.create(server_name="hexxit")
        network = Server.objects.create(server_name="network")

        nomi.save()
        e6e.save()
        ct2.save()
        ftbu.save()
        ob.save()
        hexxit.save()
        network.save()
