from src.imports import *

# Local imports.
from src.api import API
from src.objects import Creator
from src.downloader import Downloader

class Main:
    def __init__(self):
        self.api = API() # Initialise API object.

        self.links = self.get_links("data/links.txt") # Get a list of links.
        self.creators = self.get_creators(self.links)
        
        self.downloader = Downloader(creators = self.creators) # Initialising downloader object.

    def get_links(
            self,
            links_dir: str
    ) -> list[str]:
        """A function to obtain a list of links from the links.txt file.

        Args:
            links_dir (str): Path to the links.txt file.

        Returns:
            list[str]: A list of links from the links.txt file.
        """
        with open(links_dir, "r", encoding = "utf-8") as file:
            data = [x.replace("\n", "") for x in file.readlines()] # Removes the newline \n for every line.
    
        data = list(set(data)) # Create a set from the data to remove duplicate entries and then convert it back to a list.
    
        return data
    
    def get_creators(
            self,
            links: list[str]
    ) -> list[Creator]:
        """A function to retrieve a list of creator objects from a list of creator URL's.

        Args:
            links (list[str]): A list of creator URL's as a string.

        Returns:
            list[Creator]: A list of creator objects.
        """
        creators : list[Creator] = []
        
        def add_creator(url: str) -> None:
            creator = Creator(url, self.api)
            
            creators.append(creator)
            
            return
        
        threads : list[threading.Thread] = []
        for link in links:
            thread = threading.Thread(
                target = add_creator,
                args = (link, )
            )
            
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join() # Wait for threads to end before continuing.
        
        for thread in threads:
            del thread
        
        threads.clear() # Clear the list of threads.
        
        return creators