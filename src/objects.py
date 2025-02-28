from src.api import API

class File:
    def __init__(
            self,
            file_data: dict,
            api: API
    ):
        path_data_url = "https://n4.coomer.su/data"
        
        self.name : str = file_data["name"]
        self.url : str = path_data_url + file_data["path"]

class Post:
    def __init__(
            self,
            post_data: dict
    ):
        """Post object containing a post from a creator.
    
        Attributes:
            id (str): ID of the post, could match username.
            user (str): Username of the creator.
            service (str): Service the creator belongs to.
            title (str): Title of the post.
            content (str): Content in the post, usually descriptions.
            embed (dict): Containing all embeds attached to the post.
            added (str): Date the post was added to the non-creator service.
            published (str): Date the creator published the post to their service.
            files (list[File]): A list of File objects containing all files of the post.
        """
        self.id : str = post_data["id"] # ID of the post.
        self.user : str = post_data["user"] # Username of the user.
        self.service : str = post_data["service"] # Service of the creator (onlyfans, fansly)
        self.title : str = post_data["title"] # Title of the post.
        self.content : str = post_data["content"] # Content of the post (description)
        self.embed : dict = post_data["embed"] # All embeds on the post.
        self.shared_file : bool = post_data["shared_file"] # Whether the file is shared.
        self.added : str = post_data["added"] # Date the post was added to the website.
        self.published : str = post_data["published"] # Date creator added the post.
        
        self.files : list[File] = None
    
    def get_files(
        self,
        files: list[dict],
        api: API
    ) -> list[File]:
        files_obj_list : list[File] = []
        
        for file in files:
            files_obj_list.append(File(file, api))
        
        return files_obj_list

class Creator:
    def __init__(
            self,
            url: str,
            api: API
    ):
        self.url = url
        self.api = api
        
        self.service = self.get_service(self.url)
        self.id = self.get_id(self.url)
        
        creator_data = self.api.get_creator_details(self.service, self.id)
        
        self.name = creator_data["name"]
        self.indexed = creator_data["indexed"]
        self.updated = creator_data["updated"]
        
        self.posts = self.get_posts(self.service, self.id, self.api)
    
    def get_service(
            self,
            url: str
    ) -> str:
        """A function to extract a creator's service from their creator URL.

        Args:
            url (str): URL of the creator.

        Returns:
            str: Service as a string.
        """
        split_url = url.split("/")
        
        return split_url[3]

    def get_id(
            self,
            url: str
    ) -> str:
        """A function to retrieve a creator's ID from their creator URL.

        Args:
            url (str): URL of the creator.

        Returns:
            str: ID as a string.
        """
        split_url = url.split("/")
        
        return split_url[5]
    
    def get_posts(
        self,
        service: str,
        id: str,
        api: API
    ) -> list[Post]:
        """A function to retrieve a list of Post objects from a creator.

        Args:
            service (str): Service of the creator.
            id (str): ID of the creator.
            api (API): API object to get user posts.

        Returns:
            list[Post]: A list of posts.
        """
        posts : list[Post] = []
        
        for post in api.get_creator_posts(service, id):
            post_obj = Post(post)
            
            # Check if post contains attachments.
            if post["attachments"] == []: # If it doesn't.
                # Check for files.
                if post["file"] == {}: # If it doesn't.
                    continue # Skip the post.
            
                else: # If it contains files.
                    # Add the files to the post object.
                    if type(post["file"]) is not list: # If it isn't a list, change it to one.
                        post_obj.files = post_obj.get_files([post["file"]], api)
                    
                    else: # If it is, use the list.
                        post_obj.files = post_obj.get_files(post["file"], api)
            
            else: # If it contains attachments.
                # Add attachments to the post object.
                post_obj.files = post_obj.get_files(post["attachments"], api)
            
            posts.append(post_obj)
        
        return posts