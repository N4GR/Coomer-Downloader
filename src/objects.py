from src.api import API

class File:
    def __init__(
            self,
            file_data: dict
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
        
        self.files : list[File] = self._get_post_files(post_data)
    
    def _get_post_files(
            self,
            post_data: dict
    ) -> list[File]:
        attachments : list[dict] = post_data["attachments"]
        files : list[dict] | dict = post_data["file"]
        
        if type(files) is not list: files = [post_data["file"]] # Convert files to list.
        attachments.extend(files) # Combine attachments and files
        
        post_files : list[File] = []
        for file_data in attachments:
            if file_data == {}: continue # If file data is empty dictionary, continue.
            
            post_files.append(File(file_data)) # Add the file object to post_files.
        
        return post_files

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
        
        for post_data in api.get_creator_posts(service, id):
            post = Post(post_data)
            
            if len(post.files) > 0: # If there are files in the post, add it to the posts list.
                posts.append(post)
        
        return posts