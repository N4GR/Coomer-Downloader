from src.window.imports import *

# Local imports.
from src.network.api import (
    File, Creator, Post, Profile
)

from src.network.downloader import (
    Downloader, codes
)

class DownloadCreators(QThread):
    terminal_signal = Signal(str)
    complete_signal = Signal(list)
    avatar_signal = Signal(object)
    file_signal = Signal(dict)
    
    def __init__(
            self,
            links: list[str],
            output_dir: str
    ):
        super().__init__()
        self.downloader = Downloader() # Initialise downloader object.
        
        self.output_dir = output_dir
        self.active_download_workers = 0
        self.links = links
        self.lock = threading.Lock() # For thread-safe variable changes.
        self.completed_files = 0
        
        # To keep track of column and row for avatar display.
        self.row = 0
        self.column = 0
        self.max_column = 5
    
    def run(self):
        # Emit all avatar profiles to add to the display before downloading their posts.
        self.get_avatars(self.links)
        
        # Start getting creators with their posts appended.
        self.get_creators(self.links)
        
        # When complete, emit the complete signal with the links list.
        self.complete_signal.emit(self.links)
    
    def get_avatars(self, links: list[str]) -> None:
        """A function to emit an avatar to add to the avatar display.

        Args:
            links (list[str]): A list of creator links.
        """
        for link in links:
            self.avatar_signal.emit(Profile(link)) # Emit all the avatar profiles to the avatar signal to add to avatar display.
    
    def get_creators(
            self,
            links: list[str]
    ) -> None:
        for link in links:
            # Reset column if multiple of max_row.
            if self.column % self.max_column == 0:
                self.row += 1 # Add another row.
                self.column = 0 # Reset column to 0.
            
            self.terminal_signal.emit(f"GETTING POSTS | {link}")
            creator = Creator(url = link) # Gets creator object from URL.
            
            creator_dir = f"{self.output_dir}/{creator.name} [{creator.service}]"
            
            # Check if the banner exists.
            banner_dir = f"{creator_dir}/banner.png"

            if os.path.exists(banner_dir):
                self.terminal_signal.emit(f"BANNER | Present, skipping: {creator.banner}")
                
            else: # If it doesn't download it.
                self.downloader.download_banner(self.output_dir, creator)
                self.terminal_signal.emit(f"BANNER | Downloaded: {creator.banner}")
            
            # Check if the profile exists.
            profile_dir = f"{creator_dir}/profile.png"
            
            if os.path.exists(profile_dir):
                self.terminal_signal.emit(f"PROFILE | Present, skipping: {creator.image}")
            
            else: # If it doesn't, download it.
                self.downloader.download_profile(self.output_dir, creator)
                self.terminal_signal.emit(f"PRFOFILE | Downloaded: {creator.image}")

            # Emit found posts to terminal.
            self.terminal_signal.emit(f"FOUND POSTS | {len(creator.posts)} valid posts.")

            completed_posts = 1
            for post in creator.posts: # For every post in the creator object.
                self.terminal_signal.emit(f"DOWNLOADING POST | {completed_posts}/{len(creator.posts)}")
                
                self.download_post(post, creator)
                completed_posts += 1
                
                # When the post finishes downloading.
                self.terminal_signal.emit(f"POST COMPLETE | {completed_posts}/{len(creator.posts)} -> {post.title.strip().replace("\n", "")}")
    
            # When complete, add 1 to column.
            self.column += 1
            
            # Reset completed files to 0 when all files are done downloading.
            self.completed_files = 0

    def download_post(
            self,
            post: Post,
            creator: Creator
    ) -> Post:
        self.files_to_complete = len(post.files)

        # Create a thread for each file in post, the max workers concurrently working set.
        with ThreadPoolExecutor(max_workers = 10) as executor:
            for file in post.files:
                future = executor.submit(self.download_file, file, post, creator) # Submit the download_file thread to be worked.
                future.add_done_callback(self.on_file_complete) # Add onto completed_files when a file completes downloading.
        
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
        self.terminal_signal.emit(f"DOWNLOADING FILE | {file.path}")
        
        completed_downloader = self.downloader.download_file(
            self.output_dir,
            file,
            post,
            creator
        )
        
        return completed_downloader
    
    def on_file_complete(
            self,
            future: Future[tuple[File, str, int, Creator]]
    ) -> None:
        file, output_dir, code, creator = future.result() # File object and output directory string of downloaded file.
        
        with self.lock: # Add onto the completed files counter.
            self.completed_files += 1
        
        # Check codes.
        if code != 2: # If it's not a success code.
            code_text = codes[code]
            
            self.terminal_signal.emit(f"DOWNLOAD FAILED | Code {code} {code_text} -> {output_dir}") # Print error.
            return # Return function.
            
        self.terminal_signal.emit(f"DOWNLOADED FILE | {self.completed_files}/{creator.file_count} -> {output_dir}") # If all passes, print success to terminal.
        
        # Send the file complete signal to the avatar display.
        file_dict = {
            "files_complete": self.completed_files, # How many files are completed.
            "file_count": creator.file_count,
            "row": self.row, # Row of the creator the file downloaded at.
            "column": self.column
        }
        
        self.file_signal.emit(file_dict)