from src.network.imports import *

# Local imports
from src.shared.funcs import path

class API:
    def __init__(self):
        self.url = "https://coomer.su/api/v1"
        self.endpoints = self.Endpoints()
    
    class Endpoints:
        def __init__(self):
            endpoints = self._get_endpoints()
            
            self.posts = self.Posts(endpoints["Posts"])
            self.creators = self.Creators(endpoints["Creators"])
            self.comments = self.Comments(endpoints["Comments"])
            self.file = self.File(endpoints["File"])
        
        def _get_endpoints(self):
            endpoints_path = path("data/api/endpoints.yaml")
        
            with open(endpoints_path, "r", encoding = "utf-8") as file:
                endpoints = yaml.safe_load(file)
            
            return endpoints
        
        class Posts:
            def __init__(
                    self,
                    post_data: dict[str]
            ) -> None:
                self.list_all_creators : str = post_data["ListAllCreators"]
                self.list_recent_posts : str = post_data["ListRecentPosts"]
                self.list_creator_posts : str = post_data["ListCreatorPosts"]
                self.get_creator_announcements: str = post_data["GetCreatorAnnouncements"]
                self.get_post : str = post_data["GetPost"]
                self.get_post_revisions : str = post_data["GetPostRevisions"]
        
        class Creators:
            def __init__(
                    self,
                    creators_data: dict[str]
            ) -> None:
                self.get_creator : str = creators_data["GetCreator"]
                self.get_creator_linked_accounts : str = creators_data["GetCreatorLinkedAccounts"]
                self.get_creator_tags : str = creators_data["GetCreatorTags"]
        
        class Comments:
            def __init__(
                    self,
                    comments_data: dict[str]
            ) -> None:
                self.get_post_comments : str = comments_data["GetPostComments"]
        
        class File:
            def __init__(
                    self,
                    file_data: dict[str]
            ) -> None:
                self.from_hash : str = file_data["FromHash"]
    
    def get_creator_posts(
            self,
            creator_url: str
    ) -> list[dict]:
        step_count = 50 # API limit, can only get 50 posts at a time.
        current_step = 0 # Current step tracking.
        
        service = creator_url.split("https://coomer.su/")[1].split("/")[0] # Get service from url.
        creator_id = creator_url.split("/")[-1]

        endpoint = self.endpoints.posts.list_creator_posts.replace("{service}", service).replace("{creator_id}", creator_id)
        
        posts : list[dict] = []
        while True: # Create a loop to add posts to list until it can't no more.
            request = requests.get(f"{self.url}{endpoint}?o={current_step}") # Send a get request.
            print(f"Sending request: {self.url}{endpoint}?o={current_step}")
            
            if request.status_code == 200:
                post = request.json()
                
                posts.extend(post)
            
            else:
                print(f"{self.url}{endpoint}?o={current_step} failed, error: {request.status_code}")
            
            if len(post) != step_count: # If there's less posts than 50.
                break # Should indicate it was the last post, so break.
            
            current_step += step_count # Add 50 onto the step count.
        
        return posts
        
    def get_creator(
            self,
            creator_url: str
    ):
        service = creator_url.split("https://coomer.su/")[1].split("/")[0] # Get service from url.
        creator_id = creator_url.split("/")[-1]
        
        endpoint = self.endpoints.creators.get_creator.replace("{service}", service).replace("{creator_id}", creator_id)
        full_url = self.url + endpoint
        
        with requests.get(full_url) as request:
            if request.status_code == 200:
                data = request.json()
            
            else:
                print(f"Failed to get creator: {full_url}")

        creator = Creator(
            api = self,
            creator_data = data
        )
        
        return creator

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

class Creator:
    def __init__(
        self,
        api: API,
        creator_data: dict[str]
    ):
        self.id : str = creator_data["id"]
        self.name : str = creator_data["name"]
        self.service : str = creator_data["service"]
        self.indexed : str = creator_data["indexed"]
        self.updated : str = creator_data["updated"]

        self.posts, self.file_count = self._create_posts(api)
    
    def _create_posts(
            self,
            api: API
    ) -> tuple[list[Post], int]:
        """A function to retrieve and handle posts of a creator.

        Args:
            api (API): _description_

        Returns:
            list[Post]: _description_
        """
        posts_dict = api.get_creator_posts(f"https://coomer.su/{self.service}/user/{self.id}")
        
        file_counter = 0 # Count how many files are in all posts.
        posts : list[Post] = []
        for post_dict in posts_dict:
            post = Post(post_dict)
            
            if not post.files: # If there are no files, skip the post.
                continue
            
            file_counter += len(post.files)
            posts.append(post) # Append if there is files.
        
        return (posts, file_counter)