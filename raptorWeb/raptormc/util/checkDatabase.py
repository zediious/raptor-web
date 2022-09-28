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
        atm7 = Server.objects.get(server_name="atm7")
        Server.objects.get(server_name="network")

        ServerInformation.objects.get(server=nomi)
        ServerInformation.objects.get(server=e6e)
        ServerInformation.objects.get(server=ct2)
        ServerInformation.objects.get(server=ftbu)
        ServerInformation.objects.get(server=ob)
        ServerInformation.objects.get(server=atm7)
        
        LOGGER.error("[INFO] Tested for needed database objects, all are present")

    except:
        
        LOGGER.error("[WARN] Needed database entries for playerCounts.py not present. Creating them now.")

        Server.objects.all().delete()
        ServerInformation.objects.all().delete()
        
        nomi = Server.objects.create(server_name="nomi", pk=1)
        nomi_info = ServerInformation.objects.create(server=nomi, pk=1)
        e6e = Server.objects.create(server_name="e6e", pk=2)
        e6e_info = ServerInformation.objects.create(server=e6e, pk=2)
        ct2 = Server.objects.create(server_name="ct2", pk=3)
        ct2_info = ServerInformation.objects.create(server=ct2, pk=3)
        ftbu = Server.objects.create(server_name="ftbu", pk=4)
        ftbu_info = ServerInformation.objects.create(server=ftbu, pk=4)
        ob = Server.objects.create(server_name="ob", pk=5)
        ob_info = ServerInformation.objects.create(server=ob, pk=5)
        atm7 = Server.objects.create(server_name="atm7", pk=6)
        atm7_info = ServerInformation.objects.create(server=atm7, pk=6)
        network = Server.objects.create(server_name="network", pk=7)

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
        ob.save()
        ob_info.save()
        atm7.save()
        atm7_info.save()
        network.save()
