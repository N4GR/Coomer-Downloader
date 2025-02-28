from src.imports import *

class Config:
    def __init__(self):
        self.config_data = self._get_config_data()
    
        self.paths = self.Paths(self.config_data["Paths"])
        self.downloader = self.Downloader(self.config_data["Downloader"])
    
    def _get_config_data(self) -> dict:
        config_path = "data/config.yaml"
        
        with open(config_path, "r", encoding = "utf-8") as file:
            return yaml.safe_load(file)
    
    class Paths:
        def __init__(
                self,
                path_data: dict
        ):
            self.links : str = path_data["links"]
    
    class Downloader:
        def __init__(
                self,
                downloader_data: dict
        ):
            self.max_workers : int = downloader_data["max_workers"]
            self.chunk_size : int = downloader_data["chunk_size"]
            self.request_timeout : int = downloader_data["request_timeout"]
            self.stream_timeout : int = downloader_data["stream_timeout"]