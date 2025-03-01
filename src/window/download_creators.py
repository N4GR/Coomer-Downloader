from src.window.imports import *

# Local imports.
from src.network.api import (
    API, File, Creator, Post
)

from src.network.downloader import Downloader

class DownloadCreators(QThread):
    signal = Signal(str)
    
    def __init__(
            self,
            api: API,
            links: list[str],
            output_dir: str
    ):
        super().__init__()
        self.downloader = Downloader() # Initialise downloader object.
        
        self.output_dir = output_dir
        self.api = api
        self.active_download_workers = 0
        self.links = links
        self.lock = threading.Lock() # For thread-safe variable changes.
        self.completed_files = 0
    
    def run(self):
        self.get_creators(self.links)
    
    def get_creators(
            self,
            links: list[str]
    ) -> None:
        for link in links:
            self.signal.emit(f"GETTING POSTS | {links}")
            creator = self.api.get_creator(link) # Gets creator object from URL.

            completed_posts = 1
            
            self.signal.emit(f"FOUND POSTS | {len(creator.posts)}/{creator.file_count} valid posts.")
            for post in creator.posts: # For every post in the creator object.
                self.signal.emit(f"DOWNLOADING POST | {completed_posts}/{len(creator.posts)}")
                
                downloaded_post = self.download_post(post, creator)
                completed_posts += 1
                
                # When the post finishes downloading.
                self.signal.emit(f"POST COMPLETE | {completed_posts}/{len(creator.posts)} -> {post.title.strip()}")
    
    def download_post(
            self,
            post: Post,
            creator: Creator
    ) -> Post:
        self.files_to_complete = len(post.files)

        # Create a thread for each file in post, the max workers concurrently working set.
        with ThreadPoolExecutor(max_workers = 5) as executor:
            for file in post.files:
                future = executor.submit(self.download_file, file, post, creator) # Submit the download_file thread to be worked.
                future.add_done_callback(self.on_file_complete) # Add onto completed_files when a file completes downloading.
        
        # Reset completed files to 0.
        self.completed_files = 0
        
        return post
    
    def download_file(
            self,
            file: File,
            post: Post,
            creator: Creator
    ) -> tuple[File, str]:
        """A function to download a file.

        Args:
            file (File): File object of the file to download.
            post (Post): Post object that the file belongs to.
            creator (Creator): Creator object that the post / file belongs to.

        Returns:
            tuple (File, str): File object downloaded and the directory the file was downloaded to.
        """
        completed_downloader = self.downloader.download_file(
            self.output_dir,
            file,
            post,
            creator
        )
        
        return completed_downloader
    
    def on_file_complete(
            self,
            future: Future[tuple[File, str]]
    ) -> None:
        file, output_dir = future.result() # File object and output directory string of downloaded file.
        
        with self.lock: # Add onto the completed files counter.
            self.completed_files += 1
            
            self.signal.emit(f"DOWNLOADED FILE | {self.completed_files}/{self.files_to_complete} -> {output_dir}")