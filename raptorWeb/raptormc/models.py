from django.db import models

class Server(models.Model):

    server_name = models.CharField(max_length=50, default="none", unique=True)

    server_state = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.server_name

class PlayerCount(models.Model):

    server = models.ForeignKey(Server, default=0, on_delete=models.CASCADE)
    
    player_count = models.IntegerField(default=0, unique=False)

    def __str__(self) -> str:
        
        return str("Player Counts for: {}").format(self.server)

    def get_count(self):

        return self.player_count

    def get_state(self):

        return self.server_state

class PlayerName(models.Model):

    server = models.ForeignKey(Server, default=0, on_delete=models.CASCADE)

    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    
    def get_name(self):

        return self.name

    def get_server(self):

        return self.server
