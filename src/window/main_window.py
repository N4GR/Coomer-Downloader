from src.imports import *

# Local imports.
from src.window.download_creators import DownloadCreators

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
        
        # For synchronising threads.
        self.mutex = QMutex()
        self.wait_condition = QWaitCondition()
        self.active_download_workers = 0 # Keep track of download workers.
    
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
    
    def start_links_download(self, links: list[str]):
        def on_terminal(result: str) -> None:
            self.terminal.add_text(result)
        
        def on_complete(result: list[str]) -> None:
            self.terminal.add_text("PROCESSING ENDED")
            
            self.enable_interactions()
        
        def on_finished() -> None:
            "When the download worker is killed."
            self.download_worker = None # Erase the download manager QThread.
            
            self.avatar_display.reset_display() # Reset the avatar display.
            
            # Re-enable start button.
            self.side_bar.start_button.setEnabled(True)
            self.side_bar.start_button.set_to_start() # Reset the icon.
        
        def on_avatar(result: Profile) -> None:
            self.avatar_display.add_avatar(result) # Add creator to display.
        
        def on_file_complete(result: dict) -> None:
            self.avatar_display.set_avatar_file_count(result)
        
        # Start downloading a creator in a different thread.
        self.download_worker = DownloadCreators(
            links = links,
            output_dir = self.output_directory.text_edit.text()
        )
        
        self.download_worker.terminal_signal.connect(on_terminal)
        self.download_worker.complete_signal.connect(on_complete)
        self.download_worker.avatar_signal.connect(on_avatar)
        self.download_worker.file_signal.connect(on_file_complete)
        
        self.download_worker.finished.connect(on_finished)
        
        self.download_worker.start()
    
    def enable_interactions(self):
        """A function that will set all interactions to enabled."""
        self.link_input.text_edit.setEnabled(True)
        self.terminal.add_text("ENABLE | Link inputs.")
        
        self.file_input.button.setEnabled(True)
        self.terminal.add_text("ENABLE | File inputs.")
        
        self.output_directory.button.setEnabled(True)
        self.terminal.add_text("ENABLE | Output directory inputs.")
    
    def disable_interactions(self):
        """A function to halt all interactions with configurations while the start process is being handled."""
        self.link_input.text_edit.setDisabled(True)
        self.terminal.add_text("DISABLE | Link inputs.")
        
        self.file_input.button.setDisabled(True)
        self.terminal.add_text("DISABLE | File inputs.")
        
        self.output_directory.button.setDisabled(True)
        self.terminal.add_text("DISABLE | Output directory inputs.")