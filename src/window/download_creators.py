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
        def on_post_complete(future: Future):
            if self._should_stop: # Early exit.
                return
            
            with self.lock:
                self.completed_posts += 1
            
            post : Post = future.result()
            
            # When the post finishes downloading.
            self.terminal_signal.emit(f"POST COMPLETE | {self.completed_posts}/{len(creator.posts)} -> {post.title.strip().replace("\n", "")}")
        
        if self._should_stop: # Early exit.
            return
        
        # Create a thread for each post, executing a max workers to the thread.
        with ThreadPoolExecutor(max_workers = 4) as executor: # Download posts simultaenously.
                for post in creator.posts:
                    if self._should_stop: # Exit early.
                        return
                    
                    future = executor.submit(self.download_post, post, creator)
                    future.add_done_callback(on_post_complete)    
                    
    def download_post(
            self,
            post: Post,
            creator: Creator
    ) -> Post:
        def download_file(file: File, post: Post,creator: Creator) -> tuple[File, str]:
            if self._should_stop:
                return
            
            self.terminal_signal.emit(f"DOWNLOADING FILE | {file.path}")
            
            completed_downloader = self.downloader.download_file(
                self.output_dir,
                file,
                post,
                creator
            )
            
            return completed_downloader
        
        def on_file_complete(future: Future[tuple[File, str, int, Creator]]) -> None:
            if self._should_stop:
                return
            
            with self.lock: # Add onto the completed files counter.
                self.completed_files += 1
            
            file, output_dir, code, creator = future.result() # File object and output directory string of downloaded file.
            # Send the file complete signal to the avatar display.
            file_dict = {
                "files_complete": self.completed_files, # How many files are completed.
                "file_count": creator.file_count,
                "row": self.row, # Row of the creator the file downloaded at.
                "column": self.column
            }
            
            self.file_signal.emit(file_dict)
            
            # Check codes.
            if code != 2: # If it's not a success code.
                code_text = codes[code]
                
                self.terminal_signal.emit(f"DOWNLOAD FAILED | Code {code} {code_text} -> {output_dir}") # Print error.
                return # Return function.
                
            self.terminal_signal.emit(f"DOWNLOADED FILE | {self.completed_files}/{creator.file_count} -> {output_dir}") # If all passes, print success to terminal.
        
        if self._should_stop: # Early exit.
            return post
        
        self.files_to_complete = len(post.files)
        
        # Create a thread for each file in post, the max workers concurrently working set.
        with ThreadPoolExecutor(max_workers = 10) as executor:
            for file in post.files:
                if self._should_stop:
                    return
                
                future = executor.submit(download_file, file, post, creator) # Submit the download_file thread to be worked.
                future.add_done_callback(on_file_complete) # Add onto completed_files when a file completes downloading.
        
        return post
    
    def stop(self):
        """A function to safely close the QThread."""
        self.terminal_signal.emit("DOWNLOADING | STOP SIGNAL RECEIVED")
        
        with self.lock:
            self._should_stop = True