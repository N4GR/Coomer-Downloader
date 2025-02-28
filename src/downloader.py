from src.imports import *

# Local imports.
from src.objects import (
    Creator, Post
)

from src.config import Config

class Downloader:
    def __init__(
            self,
            creators: list[Creator],
            config: Config.Downloader
    ) -> None:
        self.creators = creators
        self.config = config
        
        for creator in self.creators:
            self.download_creator(creator)
    
    def download_creator(
            self,
            creator: Creator
    ) -> None:
        # Create a pool to execute concurrent threads.
        with ThreadPoolExecutor(max_workers = self.config.max_workers) as executor:
            for post in creator.posts:
                executor.submit(self.download_post, post, creator) # Submit all potential threads to executor.
            
        return
                        
    def download_post(
        self,
        post: Post,
        creator: Creator
    ):
        post_date = datetime.strptime(post.published, "%Y-%m-%dT%H:%M:%S")
        post_month_name = post_date.strftime("%B")
        post_year = post_date.strftime("%Y")
        
        for file in post.files:
            file_path = f"Downloads/{creator.name} [{creator.service}]/{post_year}/{post_month_name}/{file.name}"
            
            self.download_file(file.url, file_path)
        
        return

    def download_file(
            self,
            url: str,
            path: str
    ) -> None:
        def file_exists() -> bool:
            # Check if file already exists or not.
            if os.path.exists(path):
                return True
            
            else:
                return False
        
        def create_path() -> None:
            # Create a directory if it doesn't exist.
            directory = os.path.dirname(path)
            
            if directory and not os.path.exists(directory):
                try:
                    os.makedirs(directory) # Create the path directories if it doesn't exist.
                
                except FileExistsError as error:
                    print(error)
                    
            
            return
        
        def start_download():
            with requests.get(url, stream = True, timeout = self.config.request_timeout) as response:
                if response.status_code != 200:
                    print(f"ERROR | Request failed for {url} with status code: {response.status_code}")
                    return False  # Return early if request failed
                    
                # Open destination file in write-binary mode
                with open(path, "wb") as file:
                    last_received_time = time.time()  # Time when the last chunk was received
                    
                    # Iterate over the response in chunks to download
                    for chunk in response.iter_content(chunk_size = self.config.chunk_size):
                        if chunk:
                            file.write(chunk)
                            last_received_time = time.time()  # Reset the idle check timer
                            
                        # Check if the stream has been idle for too long
                        if time.time() - last_received_time > self.config.stream_timeout:  # 10 second idle check
                            print(f"ERROR | Stream idle for too long for {path}. Terminating download.")
                            return False  # Stop the download if idle time exceeds threshold
                    
            print(f"COMPLETE | {path}")
            return True
        
        if file_exists() is True:
            print(f"WARNING | {path} already exists, skipping.")
            
            return
    
        create_path() # Creates the path for the download.
        
        if not start_download():
            print(f"ERROR | Download failed for {path}")
            return  # Return if the download fails