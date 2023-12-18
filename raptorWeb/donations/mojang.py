from mojang import API

def verify_minecraft_username(minecraft_username: str):
    """
    Verify that a Minecraft username is a real username
    and return the UUID. Return None if no UUID is found.
    """
    api_instance = API()
    
    try:
        return api_instance.get_uuid(minecraft_username)
    
    except:
        return None
    