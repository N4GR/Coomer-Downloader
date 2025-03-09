from src.imports import *
from src.window.extensions.q_downloader import (
    QSignalEmitter, QDownloader
)

# Widgets.
from src.window.widgets.init import *

class MainWindow(QWidget):
    def __init__(
            self
    ) -> None:
        super().__init__()
        self._create_req_dirs()
        self._create_req_json()
        
        # Setting design of window.
        self._add_design()
        
        # Initialise widgets after main window design.
        self._initialise_widgets()
    
    def _create_req_dirs(self):
        """A function to create any required directories needed for the program to function (data, ect.)"""
        required_dirs = ["data"]
        
        for dir in required_dirs:
            os.makedirs(dir, exist_ok = True)
    
    def _create_req_json(self):
        """A function to create any required files used by the program (links history, ect.)"""
        def create_history():
            history_path = "data/history.json"
            
            history_dict = {
                "links": []
            }
            
            if not os.path.isfile(history_path):
                with open(history_path, "w", encoding = "utf-8") as file:
                    json.dump(history_dict, file, indent = 4)
        
        create_history()
        
    def _add_design(self):
        """A function to add design to the QWidget."""
        self.setFixedSize(1500, 600) # Sets the window to a fixed width and height.
        self.setWindowTitle("Coomer-Downloader") # Set the window title.
    
        self.setStyleSheet("background-color: rgb(33, 33, 33)") # Assigning background colour to main window.
    
        self.setWindowIcon(QIcon(path("resources/window/assets/window/icon.png"))) # Set the window icon.
    
    def _initialise_widgets(self):
        """A function to initialise all widgets assosciated with the main window; side bar, ect."""
        self.side_bar = SideBar(self)
        self.terminal = Terminal(self)
        self.link_input = LinkInput(self)
        self.file_input = FileInput(self)
        self.output_directory = OutputDirectory(self)
        self.avatar_display = AvatarDisplay(self)
        self.socials_display = SocialsDisplay(self)
    
    def start_downloader(self, links: list[str]):
        def on_avatar_found(profile: Profile):
            self.terminal.add_text(f"Avatar Found: {profile.name}")
            self.avatar_display.add_avatar(profile)
        
        self.post_thread_pool = QThreadPool(self, maxThreadCount = 3) # 3 posts concurrently.
        self.file_thread_pool = QThreadPool(self, maxThreadCount = 12) # 12 files concurrently.
        
        self.signal_emitter = QSignalEmitter(self)
        self.downloader = QDownloader(
            self.signal_emitter,
            self.terminal,
            self.post_thread_pool,
            self.file_thread_pool,
            self.output_directory.text_edit.text(),
            links,
        )
        
        self.downloader.avatar_found_signal.connect(on_avatar_found)
        self.downloader.start()