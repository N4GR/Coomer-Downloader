from src.imports import *

class Config:
    def __init__(self):
        """Config object containing data of config.
        
        Attributes:
            config_data (dict): Dictionary of config data extracted from config.yaml.
            paths (Paths): Paths object containing data related to the paths of files.
            downloader (Downloader): Downloader config object containing config for the downloader.
        """
        self.config_data = self._get_config_data()
    
        self.paths = self.Paths(self.config_data["Paths"])
        self.downloader = self.Downloader(self.config_data["Downloader"])
    
    def _get_config_data(self) -> dict:
        """A function that will get all the data pertaining to a config.yaml file.

        Returns:
            dict: Data extracted from the config.yaml file.
        """
        path = "data"
        file_name = "config.yaml"
        
        full_path = f"{path}/{file_name}"
        
        try:
            with open(full_path, "r", encoding = "utf-8") as file:
                return yaml.safe_load(file) # Returns all values from the yaml config as a dictionary.
        
        except FileNotFoundError:
            print(f"config.yaml not found in {full_path}, creating one with default values.")
            
            return self.create_config_file(
                path = path,
                file_name = file_name
            ) # Creates yaml file with default config and returns the default config as dictionary.
    
    def create_config_file(
            self,
            path: str,
            file_name: str
    ) -> dict:
        """A function that will create a default config.yaml file if it couldn't find one.

        Args:
            path (str): Path to the file without the file name attached.
            file_name (str): File name wihtout the path attached.

        Returns:
            dict: A dictionary of the default config.yaml configs.
        """
        config_comments = (
            "# Coomer-Downloader Config File.\n"
            "# Paths: All configs related to paths; where files are located.\n"
            "#    links: The path to the links file. (str)\n"
            "#\n"
            "# Downloader: All configs related to the downloader; workers, chunk size ect.\n"
            "#    max_workers: The amount of threads to be running simultaenously while downloading. (int)\n"
            "#    chunk_size: The size of each chunk in the stream when downloading in kb. (int)\n"
            "#    request_timeout: The time before ending a request to download a file in seconds. (int)\n"
            "#    stream_timeout: The time in between each stream chunk to check if the stream has been dropped in seconds. (int)\n"
        )
        
        default_config = {
            "Paths": {
                "links": "data/links.txt"
            },
            "Downloader": {
                "max_workers": 10,
                "chunk_size": 8192,
                "request_timeout": 60,
                "stream_timeout": 10
            }
        }
        
        os.makedirs(path, exist_ok = True) # Create the data path if it doesn't exist.
        
        full_path = f"{path}/{file_name}"
        with open(full_path, "w", encoding = "utf-8") as file:
            yaml.dump(default_config, file, default_flow_style = False) # Add the dictionary to yaml config.
        
        # Adding comments to YAML config.
        with open(full_path, "r+", encoding = "utf-8") as file:
            content = file.read()
            content = config_comments + "\n" + content
            
            file.seek(0)
            file.write(content)
        
        return default_config
    
    class Paths:
        def __init__(
                self,
                path_data: dict
        ):
            """A Paths object containing the locations of paths.

            Args:
                path_data (dict): Path data from the config.yaml file.
            
            Attributes:
                links (str): Path to the links.txt file.
            """
            self.links : str = path_data["links"]
    
    class Downloader:
        def __init__(
                self,
                downloader_data: dict
        ):
            """A Downloader object containing the configuration for the Downloader class.

            Args:
                downloader_data (dict): Downloader config data extracted from the config.yaml file.
            
            Attributes:
                max_workers (int): Maximum number of worker threads to concurrently download files.
                chunk_size (int): Chunk size in kb to download each chunk in a file download stream.
                request_timeout (int): Timeout of a request in seconds before it is dropped.
                stream_timeout (int): Time between stream chunks before the request is dropped in seconds.
            """
            self.max_workers : int = downloader_data["max_workers"]
            self.chunk_size : int = downloader_data["chunk_size"]
            self.request_timeout : int = downloader_data["request_timeout"]
            self.stream_timeout : int = downloader_data["stream_timeout"]