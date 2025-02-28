from src.imports import *

# Local imports.
from src.objects import (
    Creator, Post, File
)

class Downloader:
    def __init__(
            self,
            creators: list[Creator]
    ) -> None:
        self.creators = creators
        
        for creator in self.creators:
            self.download_creator(creator)
    
    def chunk_list(
            self,
            lst: list,
            chunk_size: int
    ) -> list[list[File | Post]]:
        return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]
    
    def download_creator(
            self,
            creator: Creator
    ) -> None:
        threads : list[threading.Thread] = [] # Thread storage.
        
        for chunk in self.chunk_list(creator.posts, 5): # Split posts into chunks of 5 for threading.
            for post in chunk:
                thread = threading.Thread(
                    target = self.download_post,
                    args = (post, creator)
                )
                
                thread.start()
                threads.append(thread)
            
            for thread in threads:
                thread.join() # Wait for all threads to end before continuing
            
            for thread in threads:
                del thread
            
            threads.clear() # Clear the list of threads.
        
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
            print(f"Starting download for {path}...")  # Debug start of download
            with requests.get(url, stream=True, timeout=60) as response:
                if response.status_code != 200:
                    print(f"Request failed for {url} with status code: {response.status_code}")
                    return False  # Return early if request failed
                    
                # Open destination file in write-binary mode
                with open(path, "wb") as file:
                    last_received_time = time.time()  # Time when the last chunk was received
                    print(f"Started downloading {path}")
                    
                    # Iterate over the response in chunks to download
                    for chunk in response.iter_content(chunk_size=8192):  # Chunks of 8MB
                        if chunk:
                            file.write(chunk)
                            last_received_time = time.time()  # Reset the idle check timer
                            
                        # Check if the stream has been idle for too long
                        if time.time() - last_received_time > 10:  # 10 second idle check
                            print(f"Stream idle for too long for {path}. Terminating download.")
                            return False  # Stop the download if idle time exceeds threshold
                    
            print(f"Download finished for {path}.")
            return True
        
        if file_exists() is True:
            print("The file already exists, skipping download.")
            
            return
    
        create_path() # Creates the path for the download.
        
        if not start_download():
            print(f"Download failed for {path}")
            return  # Return if the download fails