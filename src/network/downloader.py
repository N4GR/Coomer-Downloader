from src.network.imports import *

# Local imports.
from src.network.api import (
    File, Creator, Post
)

class Downloader:
    def __init__(self):
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
    ) -> tuple[File, str]:
        """A function that uses requests to download a file from a creator.

        Args:
            output_dir (str): Directory the file should be outputted to.
            file (File): File object of the file to download.
            post (Post): Post object that the file belongs to.
            creator (Creator): Creator object of the creator.
        
        Returns:
            tuple (File, str): File and output_dir of the downloaded file.
        """
        
        creator_dir = f"{output_dir}/{creator.name} [{creator.service}]"
        file_dir = f"{creator_dir}/{post.published.year}/{self.get_month_name(post.published.month)}"
        file_full_dir = f"{file_dir}/{file.name}"
        
        url = f"https://n1.coomer.su/data{file.path}"
        
        # Create the directories leading towards the output_dir.
        if not os.path.exists(file_dir):
            os.makedirs(file_dir, exist_ok = True) # Don't notify if some paths already exist.
        
        # Send a GET request to retrieve the stream of a file.
        with requests.get(url, stream = True) as response:
            # Check if the request is successful.
            if response.status_code == 200:
                # Open destination in binar-write mode.
                with open(file_full_dir, "wb") as file:
                    # Iterate over each chunk, writing it to file.
                    for chunk in response.iter_content(chunk_size = self.chunk_size):
                        file.write(chunk)
        
                return (file, file_full_dir) # Return file and output directory if successful
            
            else:
                print(f"{url} FAILED {response.status_code}")
                
                return (file, file_full_dir)
        
        return (file, file_full_dir)