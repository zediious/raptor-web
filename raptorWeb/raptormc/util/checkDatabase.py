import logging

from raptormc.models import Server, ServerInformation

def confirm_database_integrity():
    """
    Checks that Server/Server Information objects exist. If not, they will be created.
    """
    LOGGER = logging.getLogger(__name__)
    
    try:

        nomi = Server.objects.get(server_name="nomi")
        e6e = Server.objects.get(server_name="e6e")
        ct2 = Server.objects.get(server_name="ct2")
        ftbu = Server.objects.get(server_name="ftbu")
        ob = Server.objects.get(server_name="ob")
        hexxit = Server.objects.get(server_name="hexxit")
        Server.objects.get(server_name="network")

        ServerInformation.objects.get(server=nomi)
        ServerInformation.objects.get(server=e6e)
        ServerInformation.objects.get(server=ct2)
        ServerInformation.objects.get(server=ftbu)
        ServerInformation.objects.get(server=ob)
        ServerInformation.objects.get(server=hexxit)
        
        LOGGER.error("[INFO] Tested for needed database objects, all are present")

    except:
        
        LOGGER.error("[WARN] Needed database entries for playerCounts.py not present. Creating them now.")

        Server.objects.all().delete()
        ServerInformation.objects.all().delete()
        
        nomi = Server.objects.create(server_name="nomi")
        nomi_info = ServerInformation.objects.create(server=nomi)
        e6e = Server.objects.create(server_name="e6e")
        e6e_info = ServerInformation.objects.create(server=e6e)
        ct2 = Server.objects.create(server_name="ct2")
        ct2_info = ServerInformation.objects.create(server=ct2)
        ftbu = Server.objects.create(server_name="ftbu")
        ftbu_info = ServerInformation.objects.create(server=ftbu)
        ob = Server.objects.create(server_name="ob")
        ob_info = ServerInformation.objects.create(server=ob)
        hexxit = Server.objects.create(server_name="hexxit")
        hexxit_info = ServerInformation.objects.create(server=hexxit)
        network = Server.objects.create(server_name="network")

        nomi.save()
        nomi_info.save()
        e6e.save()
        e6e_info.save()
        ct2.save()
        ct2_info.save()
        ftbu.save()
        ftbu_info.save()
        ob.save()
        ob_info.save()
        hexxit.save()
        hexxit_info.save()
        network.save()
