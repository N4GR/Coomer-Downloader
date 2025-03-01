from src.window.imports import *

# Local imports.
from src.shared.funcs import path
from src.network.api import API
from src.window.download_creators import DownloadCreators

# Widgets.
from src.window.sidebar import SideBar
from src.window.terminal import Terminal
from src.window.link_input import LinkInput
from src.window.file_input import FileInput
from src.window.output_directory import OutputDirectory
from src.window.avatar_display import AvatarDisplay

class MainWindow(QWidget):
    def __init__(
            self
    ) -> None:
        super().__init__()
        self.api = API() # Initialise API object.
        
        # Setting design of window.
        self._add_design()
        
        # Initialise widgets after main window design.
        self._initialise_widgets()
        
        # For synchronising threads.
        self.mutex = QMutex()
        self.wait_condition = QWaitCondition()
        self.active_download_workers = 0 # Keep track of download workers.
    
    def _add_design(self):
        """A function to add design to the QWidget."""
        self.setFixedSize(1500, 600) # Sets the window to a fixed width and height.
        self.setWindowTitle("N4GR - Coomer-Downloader") # Set the window title.
    
        self.setStyleSheet("background-color: rgb(33, 33, 33)") # Assigning background colour to main window.
    
        self.setWindowIcon(QIcon(path("data/window/assets/window/icon.png"))) # Set the window icon.
    
    def _initialise_widgets(self):
        """A function to initialise all widgets assosciated with the main window; side bar, ect."""
        self.side_bar = SideBar(self)
        self.terminal = Terminal(self)
        self.link_input = LinkInput(self)
        self.file_input = FileInput(self)
        self.output_directory = OutputDirectory(self)
        self.avatar_display = AvatarDisplay(self)
        
        # Creating a connection for file input to interact with main window.
        self.file_input.button.clicked.connect(self.on_file_input_clicked)
        
        # Creating a connection for output directory to interact with the main window.
        self.output_directory.button.clicked.connect(self.on_output_dir_clicked)
        
        # Cerating a connection for the start button to interact with the main window.
        self.side_bar.start_button.clicked.connect(self.on_start_clicked)
        
    def on_file_input_clicked(self):
        # Open the explorer to retrieve a text file.
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Text File", "", "Text Files (*.txt)")
        
        # If a file is selected, add it to the file_input text and add a terminal log entry.
        if file_path:
            self.file_input.text_edit.setText(file_path)
            self.terminal.add_text(f"Set {file_path} as links document.")
    
    def on_output_dir_clicked(self):
        dir_name = QFileDialog.getExistingDirectory(self, "Select output directory")
        
        # If the directory is selected, add it to the output_directory text input and log it to terminal.
        if dir_name:
            self.output_directory.text_edit.setText(dir_name)
            self.terminal.add_text(f"Set {dir_name} as output directory.")
    
    def on_start_clicked(self):
        def check_output_directory() -> bool:
            """A function that will check an output directory - returning False if it failed.

            Returns:
                bool: True | False - whether the check failed: False, or passed: True.
            """
            output_dir = self.output_directory.text_edit.text()
            
            if not output_dir: # If no output directory is selected.
                self.terminal.add_text(f"Output directory not selected.")
                
                message = QMessageBox(self) # Create a message box.
                message.setIcon(QMessageBox.Icon.Warning)
                message.setWindowTitle("Directory Selection Needed")
                message.setText("You need to select an output directory.")
                message.setInformativeText("Please choose a valid directory to download the posts to.")
                message.setStandardButtons(QMessageBox.StandardButton.Ok)
                
                message.exec_() # Execute warning message.
                
                return False # Return false.
            
            else:
                if not os.path.exists(output_dir): # If the path doesn't exist.
                    self.terminal.add_text(f"{output_dir} is invalid.")
                    
                    message = QMessageBox(self)
                    message.setIcon(QMessageBox.Icon.Critical)
                    message.setWindowTitle("Invalid Ouput Directory")
                    message.setText("You entered an invalid output directory.")
                    message.setInformativeText("The output directory you selected was invalid; it doesn't exist.")
                    message.setStandardButtons(QMessageBox.StandardButton.Ok)
                    
                    message.exec_()
                    
                    return False
                
                else: # If the path exists.
                    return True # Pass the check.

        def check_inputted_links() -> bool:
            """A function to check if the user has given a links file or inputted links.

            Returns:
                bool: True | False whether the links are there or not.
            """
            
            link_file_dir = self.file_input.text_edit.text()
            link_inputs = self.link_input.text_edit.toPlainText()
            
            if not link_file_dir: # If no links file provided.
                if not link_inputs: # If there's no links in the text box.
                    # This means the user has not added ANY links.
                    message = QMessageBox(self)
                    message.setIcon(QMessageBox.Icon.Critical)
                    message.setWindowTitle("No Links Added")
                    message.setText("You need to input links of creators to be downloaded.")
                    message.setStandardButtons(QMessageBox.StandardButton.Ok)
                    
                    message.exec_() # Execute message box.

                    self.terminal.add_text("NO LINKS | No links found.")

                    return False # Return False.
                    
                else: # There's no links file, but there's link in the input.
                    return True
            
            else: # There's a link file provided and link inputs haven't been checked.
                return True

        def get_links_from_file() -> list[str]:
            """A function to get a list of strings from the links file input.

            Returns:
                list[str]: A list of strings from the file input.
            """
            with open(self.file_input.text_edit.text(), "r", encoding = "utf-8") as file:
                # Read each line, remove the comma, and strip the spaces.
                links_from_file = [line.strip().replace(",", "") for line in file.readlines()]
            
            return links_from_file

        def print_link_findings(
                link_inputs: list,
                links_from_file: list | None
        ) -> None:
            """A function that will print any findings from the links to terminal.

            Args:
                link_inputs (list): _description_
                links_from_file (list | None): _description_
            """
            # If there's links from file.
            if links_from_file:
                for link in links_from_file:
                    self.terminal.add_text(f"LINK FOUND | {link} in {self.file_input.text_edit.text()}") # Add the finding to terminal.
            
            # If there's links from the text edit.
            if len(link_inputs) > 0:
                for link in link_inputs:
                    self.terminal.add_text(f"LINK FOUND | {link}")
        
        def clean_links(links: list[str]) -> list[str]:
            """A function that will check each link over the current URL's to see if they're valid or not.

            Args:
                links (list[str]): A list of links wanting to be downloaded.

            Returns:
                list[str]: A fixed list of url's if necessary.
            """
            coomer_url = "https://coomer.su"
            fixed_links : list[str] = []
            
            for link in links:
                if coomer_url in link:
                    fixed_links.append(link)
                    
                    self.terminal.add_text(f"VALID LINK | {link}")
                
                else:
                    self.terminal.add_text(f"INVALID LINK | {link}")
            
            return fixed_links
        
        if check_output_directory() is False: return
        if check_inputted_links() is False: return
        
        self.terminal.add_text("Starting processes...")
        self.disable_interactions() # Disable interactions before starting processes.
        
        links = [link.strip() for link in self.link_input.text_edit.toPlainText().split(",")] # Get a list of items given in link input.
        links_from_file = []
        
        # Read the links in the file input.
        if self.file_input.text_edit.text(): # If there's a file wanting to be parsed.
            links_from_file = get_links_from_file()
        
        print_link_findings(
            link_inputs = links,
            links_from_file = links_from_file
        ) # Print any link findings to the terminal.
        
        links.extend(links_from_file) # Add links from file onto the links list.
        links = clean_links(links)
        
        # If the links list is empty after cleaning, create a warning message and end downloading.
        if len(links) <= 0:
            message = QMessageBox(self)
            message.setIcon(QMessageBox.Icon.Critical)
            message.setWindowTitle("All Links Invalid")
            message.setText("All links you entered have been marked as invalid.")
            message.setStandardButtons(QMessageBox.StandardButton.Ok)
            
            message.exec_() # Execute message box.

            self.terminal.add_text("NO LINKS | No links found.")
            
            self.enable_interactions() # Re-enable all interactions.
            return
        
        self.start_links_download(links) # Start the creator threads to get creators.
    
    def start_links_download(self, links: list[str]):
        output_dir = self.output_directory.text_edit.text()
        
        # Start downloading a creator in a different thread.
        self.download_worker = DownloadCreators(self.api, links, output_dir)
        self.download_worker.signal.connect(self.on_download_signal)
        self.download_worker.complete_signal.connect(self.on_all_complete)
        self.download_worker.start()
    
    def on_download_signal(
            self,
            result: str
    ) -> None:
        self.terminal.add_text(result)
    
    def on_all_complete(
            self,
            result: list[str]
    ) -> None:
        self.terminal.add_text(f"PROCESSES COMPLETE | {len(result)} creators.")
        
        self.enable_interactions()
    
    def enable_interactions(self):
        """A function that will set all interactions to enabled."""
        self.side_bar.start_button.setEnabled(True)
        self.terminal.add_text("ENABLE | Start button.")
        
        self.link_input.text_edit.setEnabled(True)
        self.terminal.add_text("ENABLE | Link inputs.")
        
        self.file_input.button.setEnabled(True)
        self.terminal.add_text("ENABLE | File inputs.")
        
        self.output_directory.button.setEnabled(True)
        self.terminal.add_text("ENABLE | Output directory inputs.")
    
    def disable_interactions(self):
        """A function to halt all interactions with configurations while the start process is being handled."""
        self.side_bar.start_button.setDisabled(True)
        self.terminal.add_text("DISABLE | Start button.")
        
        self.link_input.text_edit.setDisabled(True)
        self.terminal.add_text("DISABLE | Link inputs.")
        
        self.file_input.button.setDisabled(True)
        self.terminal.add_text("DISABLE | File inputs.")
        
        self.output_directory.button.setDisabled(True)
        self.terminal.add_text("DISABLE | Output directory inputs.")