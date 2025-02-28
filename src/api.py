from src.imports import *

class Paths:
    def __init__(self):
        """A Paths object that contains data related to the API paths.
        
        Attributes:
            url (str): Base URL for the API.
            posts (Posts): Posts object that will contain endpoints related to posts.
            file (File): File object that will contain endpoints related to files.
            creator (Creator): Creator object that will contain endpoints related to a creator.
        """
        self.url = "https://coomer.su/api/v1"
        self.posts = self.Posts()
        self.file = self.File()
        self.creator = self.Creator()
            
    class Posts:
        def __init__(self):
            """Posts object containing endpoints related to posts.
            
            Attributes:
                from_user (str): The endpoint to get posts from a user.
            """
            self.from_user = "/{service}/user/{creator_id}"
    
    class File:
        def __init__(self):
            """File object containing endpoints related to files.
            
            Attributes:
                from_hash (str): The endpoint to get file data from its hash.
            """
            self.from_hash = "/search_hash/{file_hash}"

    class Creator:
        def __init__(self):
            """Creator object containing endpoints related to creators.
            
            Attributes:
                from_id (str): The endpoint to get profile data of a creator from their id.
            """
            self.from_id = "/{service}/user/{creator_id}/profile"

class API:
    def __init__(self):
        """API Object that will handle all functions related to the API.
        
        Attributes:
            paths (Paths): Paths object containing data related to the API URL and endpoints.
        """
        self.paths = Paths()
    
    def get_creator_posts(
        self,
        service: str,
        creator_id: str
    ) -> list[dict]:
        """A function that will iterate through a creators profile to get all posts, using the API offset limit of 50.

        Args:
            service (str): Service the creator belongs to as a string.
            creator_id (str): ID of the creator as a string.

        Returns:
            list[dict]: List of dictionaries which are posts.
        """
        offset = 0 # To measure which posts to grab.
        step_limit = 50 # Enforced by API.
        
        endpoint = self.paths.posts.from_user.replace("{service}", service).replace("{creator_id}", creator_id) # Replace the endpoint variables with the necessary strings.
        url = self.paths.url + endpoint # Full URL of the API to check a creator.
        
        response_data : list[dict] = []
        while True:
            url = self.paths.url + endpoint + f"?o={offset}" # URL with enforced offset.

            print(f"API | Sending request: {url}")
            response = requests.get(url) # Perform GET request.

            if response.status_code == 200:
                response_data.extend(response.json()) # Add the items onto the list.
                
                if len(response.json()) < step_limit: # Break loop if the amount of posts is less than step_limit, indicating last page.
                    break
                
                offset += step_limit
    
        return response_data
    
    def get_creator_details(
        self,
        service: str,
        creator_id: str
    ) -> dict:
        """A function to retrieve details about a creator.

        Args:
            service (str): Service of the creator.
            creator_id (str): ID of the creator (sometimes username).

        Returns:
            dict: Dictionary data of creator.
        """
        endpoint = self.paths.creator.from_id.replace("{service}", service).replace("{creator_id}", creator_id)
        url = self.paths.url + endpoint
        
        response = requests.get(url)
        
        if response.status_code == 200:
            return response.json()