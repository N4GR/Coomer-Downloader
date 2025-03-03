# RUNS ON ITS OWN.

from datetime import datetime
import requests
from src.network.endpoints import Endpoints

endpoints = Endpoints()
coomer_api_url = endpoints.servers.coomer.api

class File:
    def __init__(
            self,
            file_data: dict
    ) -> None:
        self.name = file_data["name"]
        self.path = file_data["path"]

class Post:
    def __init__(
            self,
            post_dict: dict
    ) -> None:
        self.id : str = post_dict["id"]
        self.title : str = post_dict["title"]
        self.content : str = post_dict["content"]
        self.added : datetime = datetime.strptime(post_dict["added"].split(".")[0], "%Y-%m-%dT%H:%M:%S") # Remove ms from time.
        self.published : datetime = datetime.strptime(post_dict["published"].split(".")[0], "%Y-%m-%dT%H:%M:%S") # Remove ms from time.
        self.files : list[File] = self._get_files(post_dict)
    
    def _get_files(
            self,
            post_dict: dict
    ) -> list[File]:
        files = [post_dict["file"]]
        attachments = post_dict["attachments"]

        files.extend(attachments) # Add the attachments list to the files list.
        
        file_list : list[File] | None = []
        for file in files:
            if file == {}: # If file is an empty dictionary, skip.
                continue
            
            file_list.append(File(file))
        
        return file_list

class Profile:
    def __init__(self, url: str):
        """A class object which is a profile of a user; doesn't contain their posts.

        Args:
            url (str): URL of the user.
        """
        self.url = url
        
        data = self._get_profile_data()
        self.id : str = data["id"]
        self.name : str = data["name"]
        self.service : str = data["service"]
        self.indexed : str = data["indexed"]
        self.updated : str = data["updated"]
        
        self.image : str = endpoints.servers.coomer.icon.replace("{service}", self.service).replace("{creator_id}", self.id)
        self.banner : str = endpoints.servers.coomer.banner.replace("{service}", self.service).replace("{creator_id}", self.id)
    
    def _get_profile_data(self) -> dict:
        service = self.url.split("/")[-3] # https://coomer.su/onlyfans/user/belledelphine -> onlyfans
        id = self.url.split("/")[-1] # https://coomer.su/onlyfans/user/belledelphine -> belledelphine
        
        url = endpoints.servers.coomer.api + endpoints.creator.profile.replace("{service}", service).replace("{creator_id}", id)
        
        print(url)
        # Send a GET request to obtain the profile data.
        with requests.get(url) as response:
            if response.status_code == 200:
                return response.json()
            
            else:
                return None

class Creator(Profile):
    def __init__(self, url: str):
        super().__init__(url)
        """A subclass of profile, a creator is someone who contains posts.
        
        Args:
            url (str): URL of the user.
        """
        
        self.posts = self._get_posts()
        self.file_count = self._get_file_count()
    
    def _get_posts(self) -> list[Post]:
        step_count = 50 # Enforced by API.
        current_step = 0 # Step storage.
        
        url = endpoints.servers.coomer.api + endpoints.creator.posts.replace("{service}", self.service).replace("{creator_id}", self.id)
        
        pages : list[dict] = [] # Page storage.
        while True:
            # Send a GET request for the posts.
            with requests.get(f"{url}?o={current_step}") as response:
                if response.status_code == 200:
                    page = response.json()
                    pages.extend(page) # Add post dict list onto posts.
                
                if len(page) != step_count: # Signifies last page.
                    break
                
                else:
                    current_step += step_count # Add onto step_count to next page.
        
        # Create the Post list object.
        posts : list[Post] = []
        for post_dict in pages:
            post = Post(post_dict)
            
            # If no files are found, don't add it to the posts.            
            if not post.files:
                continue
            
            else:
                posts.append(post) # Add onto the post list.
        
        # Return the list of posts.
        return posts
            
    def _get_file_count(self) -> int:
        file_counter = 0
        
        for post in self.posts:
            for file in post.files:
                file_counter += 1
        
        return file_counter