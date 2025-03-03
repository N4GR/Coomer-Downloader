from src.network.imports import *

# Local imports.
from src.network.api import (
    File, Creator, Post
)

from src.network.endpoints import Endpoints

# For handling PySide requests.
from src.window.imports import (
    QBuffer, QByteArray, QPixmap, QIODevice
)

codes = {
    1: "File exists.",
    2: "Success.",
    3: "Request denied.",
    4: "Failed request."
}

class Downloader:
    def __init__(self):
        self.endpoints = Endpoints() # Load endpoints object.
        
        self.lock = threading.Lock()
        
        self.chunk_size = 8192

    def get_month_name(
        self,
        month: int
    ) -> str:
        """A function to get the name of a month from its int number.

        Args:
            month (int): Number of the month, 1-12

        Returns:
            str: Name of the month, January-December
        """
        month_to_name = {
            1: "January",
            2: "February",
            3: "March",
            4: "April",
            5: "May",
            6: "June",
            7: "July",
            8: "August",
            9: "September",
            10: "October",
            11: "November",
            12: "December"
        }
        
        return month_to_name[month]

    def download_file(
        self,
        output_dir: str,
        file: File,
        post: Post,
        creator: Creator
    ) -> tuple[File, str, int, Creator]:
        """A function that uses requests to download a file from a creator.

        Args:
            output_dir (str): Directory the file should be outputted to.
            file (File): File object of the file to download.
            post (Post): Post object that the file belongs to.
            creator (Creator): Creator object of the creator.
        
        Returns:
            tuple (File, str): File and output_dir of the downloaded file.
        """

        # {output_dir}/BelleDelphine [onlyfans]
        creator_dir = f"{output_dir}/{creator.name} [{creator.service}]"
        
        # {output_dir}/BelleDelphine [onlyfans]/2025/01
        file_dir = f"{creator_dir}/{post.published.year}/{self.get_month_name(post.published.month)}"
        
        # {output_dir}/BelleDelphine [onlyfans]/2025/01/file.png
        file_full_dir = f"{file_dir}/{file.name}"
        
        url = self.endpoints.servers.coomer.download.replace("{file_path}", file.path)
        
        # Create the directories leading towards the output_dir.
        if not os.path.exists(file_dir):
            os.makedirs(file_dir, exist_ok = True) # Don't notify if some paths already exist.
        
        # If the file already exists, return file, full_dir and code 1.
        if os.path.exists(file_full_dir):
            return (file, file_full_dir, 1, creator) # Code 1: File already exists.

        def download_chunk(file: BufferedWriter, chunk: bytes):
            with self.lock:
                file.write(chunk) # Thread-safe writing.
        
        with requests.get(url, stream = True) as response: # Send GET request for file stream.
            if response.status_code == 200:
                with open(file_full_dir, "wb") as file: # Open file in byte-write mode.
                    with ThreadPoolExecutor(max_workers = 4) as executor: # Create a thread pool to download chunks.
                        for chunk in response.iter_content(self.chunk_size):
                            executor.submit(download_chunk, file, chunk) # Downloads each chunk in threads.

                return (file, file_full_dir, 2, creator)
            
            else:
                return (file, file_full_dir, 4, creator)
                
        return (file, file_full_dir, 3, creator)

    def download_profile(
            self,
            output_dir: str,
            creator: Creator
    ):
        # {output_dir}/BelleDelphine [onlyfans]
        creator_dir = f"{output_dir}/{creator.name} [{creator.service}]"
        
        # {output_dir}/BelleDelphine [onlyfans]/profile.png
        profile_dir = f"{creator_dir}/profile.png"
        
        # Create the path to creator_dir if it doesn't exist.
        os.makedirs(creator_dir, exist_ok = True)
        
        with requests.get(creator.image, stream = True) as response:
            if response.status_code == 200:
                with open(profile_dir, "wb") as file:
                    for chunk in response.iter_content(chunk_size = self.chunk_size):
                        file.write(chunk)
                
                return True
            
            else:
                return False
        
        return False
    
    def download_banner(
            self,
            output_dir: str,
            creator: Creator
    ):
        # {output_dir}/BelleDelphine [onlyfans]
        creator_dir = f"{output_dir}/{creator.name} [{creator.service}]"
        
        # {output_dir}/BelleDelphine [onlyfans]/banner.png
        profile_dir = f"{creator_dir}/banner.png"
        
        # Create the path to creator_dir if it doesn't exist.
        os.makedirs(creator_dir, exist_ok = True)
        
        with requests.get(creator.banner, stream = True) as response:
            if response.status_code == 200:
                with open(profile_dir, "wb") as file:
                    for chunk in response.iter_content(chunk_size = self.chunk_size):
                        file.write(chunk)
                
                return True
            
            else:
                return False
        
        return False
    
def get_pixmap_from_url(url: str) -> QPixmap:
    with requests.get(url) as response:
        if response.status_code == 200:
            byte_array = QByteArray(response.content)
            
            # Create a QBuffer for the byte_array in readonly mode.
            buffer = QBuffer(byte_array)
            buffer.open(QIODevice.OpenModeFlag.ReadOnly)
            
            # Load the image from buffer into a QPixmap.
            pixmap = QPixmap()
            if pixmap.loadFromData(byte_array):
                return pixmap # Return the generated pixmap.