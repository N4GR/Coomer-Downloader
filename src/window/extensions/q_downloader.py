from src.imports import *

# Type-hinting.
from src.window.widgets.terminal import Terminal

class QSignalEmitter(QObject):
    file_progress_signal = Signal(dict)
    def emit_file_progress(
            self,
            creator: Creator,
            post: Post,
            file: File,
            file_size: int,
            mbps: int
    ):
        
        progress_dict = {
            "creator": creator,
            "post": post,
            "file": file,
            "file_size": file_size,
            "mbps": mbps
        }
        
        self.file_progress_signal.emit(progress_dict)
        
class QDownloader(QThread):
    def __init__(
            self,
            signal_emitter: QSignalEmitter,
            terminal_display: Terminal,
            post_thread_pool: QThreadPool,
            file_thread_pool: QThreadPool,
            output_directory: str,
            links: list[str]
    ):
        super().__init__()
        self.signal_emitter = signal_emitter
        
        self.post_thread_pool = post_thread_pool
        self.file_thread_pool = file_thread_pool
        self.terminal = terminal_display
        self.links = links
        self.output_directory = output_directory
        
        # Tracking column and row for avatar display.
        self.row = 0
        self.column = 0
        self.max_column = 5
        
        self.post_mutex = QMutex()
        self.post_wait_condition = QWaitCondition()
        
        self.file_mutex = QMutex()
        self.file_wait_condition = QWaitCondition()
        self.endpoints = Endpoints()
        
        self.mutex = QMutex()
        self.wait_condition = QWaitCondition()
    
    def run(self):
        self.get_avatars()
        self.get_creators()
    
    avatar_found_signal = Signal(object)
    def get_avatars(self):
        for link in self.links:
            self.terminal.add_text(f"Getting avatar: {link}")
            
            profile = Profile(link)
            self.avatar_found_signal.emit(profile)
            
            self.terminal.add_text(f"Avatar Found: {profile.image}")
    
    def get_creators(self):
        self.file_downloaders : list[QDownloader.QDownloadFile] = []
        
        for link in self.links:
            creator = Creator(link)
            
            for post in creator.posts:
                for file in post.files:
                    self.download_file = self.QDownloadFile(
                        self.terminal,
                        self.signal_emitter,
                        self.file_mutex,
                        self.file_thread_pool,
                        creator,
                        file,
                        post,
                        self.output_directory,
                        self.endpoints,
                        self.row,
                        self.column
                    )
                    
                    self.file_downloaders.append(self.download_file)
                    self.file_thread_pool.start(self.download_file)
            
                # Empty downloaders list when post ends.
                self.file_downloaders = []
            
            # Wait for the signal to retrieve next creator.
            if self.column % self.max_column == 0: # If current column is a multiple of max_col, reset col to 0.
                self.row += 1
                self.column = 0
            
            self.column += 1
            
            self.mutex.lock()
            self.wait_condition.wait(self.mutex)
            self.mutex.unlock()
    
    class QDownloadFile(QRunnable):
        def __init__(
                self,
                terminal: Terminal,
                signal_emitter: QSignalEmitter,
                mutex: QMutex,
                wait_condition: QWaitCondition,
                creator: Creator,
                file: File,
                post: Post,
                output_directory: str,
                endpoints: Endpoints,
                row: int,
                column: int
        ):
            super().__init__()
            self.terminal = terminal
            
            self.signal_emitter = signal_emitter
            self.mutex = mutex
            self.wait_condition = wait_condition
            
            self.creator = creator
            self.file = file
            self.post = post
            
            self.output_directory = output_directory
            self.endpoint = endpoints
            
            self.row = row
            self.column = column
                    
        def run(self):
            url = self.endpoint.servers.coomer.download.replace("{file_path}", self.file.path)
            
            # C:/Downloads/BelleDelphine [onlyfans]/
            creator_dir = f"{self.output_directory}/{self.creator.name} [{self.creator.service}]"
            
            # C:/Downloads/BelleDelphine [onlyfans]/2025/April
            file_base_dir = f"{creator_dir}/{self.post.published.year}/{self.post.published.strftime('%B').capitalize()}"
            
            # C:/Downloads/BelleDelphine [onlyfans]/2025/April/dsfhdsiufds.png
            file_dir = f"{file_base_dir}/{self.file.name}"
            
            # Create the directories leading towards the file.
            if not os.path.exists(file_base_dir):
                os.makedirs(file_base_dir, exist_ok = True)
            
            if os.path.exists(file_dir):
                #self.terminal.add_text(f"File exists, skipping {file_dir}")
                
                self.signal_emitter.emit_file_progress(
                    self.creator,
                    self.post,
                    self.file,
                    0,
                    0
                )
                
                time.sleep(0.001) # FUCK PYSIDE, I HAVE TO DO THIS SO IT DOESN'T GET CONFUSED AND NOT RETURN PROPERLY!
                
                return

            print("Downloading file")
            
            chunk_size = 32768 # Size of each chunk to download in.
            # Initialize timing and tracking variables
            start_time = time.time()
            last_report_time = start_time
            downloaded = 0  # Track total bytes downloaded
            bytes_since_last_report = 0  # Track bytes downloaded since last report
            download_speed_mbps = 0
            
            # Start downloading the file
            with requests.get(url, stream=True) as response:
                response.raise_for_status()  # Raise an error if the HTTP request fails

                file_size = int(response.headers.get("Content-Length", 0))  # File size in bytes

                # Open the file for writing the chunks
                with open(file_dir, "wb") as file:
                    for chunk in response.iter_content(chunk_size=chunk_size):
                        # Write the chunk to the file
                        file.write(chunk)
                        downloaded += len(chunk)
                        bytes_since_last_report += len(chunk)

                        # If 1 second has passed, calculate the speed
                        if time.time() - last_report_time >= 1:
                            # Calculate download speed in Mbps (megabits per second)
                            elapsed_time = time.time() - last_report_time
                            download_speed_mbps = (bytes_since_last_report * 8) / elapsed_time / 1_000_000

                            # Reset the last report time and the byte counter
                            last_report_time = time.time()
                            bytes_since_last_report = 0  # Reset the counter for the next second
            
            self.signal_emitter.emit_file_progress(
                self.creator,
                self.post,
                self.file,
                file_size,
                download_speed_mbps
            )
            
            time.sleep(0.001) # FUCK PYSIDE, I HAVE TO DO THIS SO IT DOESN'T GET CONFUSED AND NOT RETURN PROPERLY!
            
            self.terminal.add_text(f"File complete: {url}")