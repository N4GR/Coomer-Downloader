# RUNS ON ITS OWN.

import json
from src.shared.funcs import path

class Endpoints:
    def __init__(self):
        data = self._get_data()
    
        self.servers = self.Servers(data["servers"])
        self.creator = self.Creator(data["creator"])
    
    def _get_data(self) -> dict:
        with open(path("data/api/endpoints.json"), "r", encoding = "utf-8") as file:
            return json.load(file)
    
    class Servers:
        def __init__(self, servers_data: dict):
            self.coomer = self.Server(servers_data["coomer"])
            self.kemono = self.Server(servers_data["kemono"])
        
        class Server:
            def __init__(self, server_data: dict):
                self.api : str = server_data["api"]
                self.download : str = server_data["download"]
                self.icon : str = server_data["icon"]
                self.banner : str = server_data["banner"]
    
    class Creator:
        def __init__(self, creator_data: dict):
            self.posts : str = creator_data["posts"]
            self.tags : str = creator_data["tags"]
            self.profile : str = creator_data["profile"]
            self.accounts : str = creator_data["accounts"]
            self.fancards : str = creator_data["fancards"]
            self.announcements : str = creator_data["announcements"]

            self.file : str = creator_data["file"]

            self.post = self.Post(creator_data["post"])

        class Post:
            def __init__(self, post_data: dict):
                self.from_id : str = post_data["from_id"]
                self.revisions : str = post_data["revisions"]
                self.comments : str = post_data["comments"]