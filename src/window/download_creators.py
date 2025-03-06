from src.imports import *

# Local imports.
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
        
        self._should_stop = False # Flag to indicate if threads should stop.
        self._mutex = QMutex() # Ensure thread-safety.
        
        self.output_dir = output_dir
        self.active_download_workers = 0
        self.links = links
        self.lock = threading.Lock() # For thread-safe variable changes.
        self.completed_files = 0
        self.completed_posts = 0
        
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
            if self._should_stop: # Early exit.
                return
            
            self.avatar_signal.emit(Profile(link)) # Emit all the avatar profiles to the avatar signal to add to avatar display.
    
    def get_creators(
            self,
            links: list[str]
    ) -> None:
        for link in links:
            if self._should_stop: # Exit early.
                return
            
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

            self.download_posts(creator) # Send the creator to the posts threading to download posts.
            
            self.column += 1 # Add 1 to column for next avatar display.
            self.completed_files = 0 # Reset value.
            self.completed_posts = 0 # Reset value.

    def download_posts(
            self,
            creator: Creator
    ) -> None:
        def on_file_complete(result: dict):
            with self.lock: # Add numbers with lock, for thread-safe operation.
                self.column += 1
                
                if self.column % self.max_column == 0: # If current column is a multiple of max_col, reset col to 0.
                    self.row += 1
                    self.column = 0
        
                file_dict = {
                    "row": self.row,
                    "column": self.column,
                    "files_complete": self.completed_files,
                    "file_count": self.file_count
                }
                
                self.file_signal.emit(file_dict)
        
        if self._should_stop: # Early exit.
            return
        
        for post in creator.posts:
            with ThreadPoolExecutor(max_workers = len(post.files)) as executor: # A thread for each file.
                self.file_count = len(post.files)
                
                for file in post.files:
                    worker = DownloadFile()
                    worker.file_progress_signal.connect()
                    worker.file_complete_signal.connect(on_file_complete)

            # When the post finishes downloading.
            self.completed_posts += 1
            self.terminal_signal.emit(f"POST COMPLETE | {self.completed_posts}/{len(creator.posts)} -> {post.title.strip().replace("\n", "")}")
            
    def stop(self):
        """A function to safely close the QThread."""
        self.terminal_signal.emit("DOWNLOADING | STOP SIGNAL RECEIVED")
        
        with self.lock:
            self._should_stop = True

class DownloadFile(QThread):
    file_progress_signal = Signal(str)
    file_complete_signal = Signal(dict)
    
    def __init__(
            self,
            file: File
    ):
        super().__init__()
        self.file = file
    
    def run(self):
        pass