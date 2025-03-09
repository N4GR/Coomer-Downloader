from src.imports import *

class SideBar(QWidget):
    def __init__(
            self,
            parent: QWidget
    ) -> None:
        super().__init__(parent)
        # Setting design of window.
        self._add_design()
        
        # Initialise widgets after main window design.
        self._initialise_widgets()
    
    def _add_design(self):
        """A function to add design to the QWidget."""
        self.setFixedSize(100, 600) # Assigning size to Widget.
        self.move(0, 0) # Moving widget to top left of main window.
    
    def _initialise_widgets(self):
        """A function to initialise all widgets assosciated with the main window; background label, ect."""
        self.background_label = self.BackgroundLabel(self)
        self.start_button = self.StartButton(self)

    class BackgroundLabel(QLabel):
        def __init__(
                self,
                parent: QWidget
        ) -> None:
            super().__init__(parent)
            self._add_design()
        
        def _add_design(self):
            self.setFixedSize(100, 600) # Assigning size to label.
            self.setStyleSheet(f"background-color: rgb(47, 47, 47)") # Assigning background colour to label.

            # Select a random mascot from the provided images.
            mascot = random.choice([
                path("resources/window/assets/window/mascots/") + mascot
                for mascot
                in os.listdir(path("resources/window/assets/window/mascots"))
            ])
            
            self.setPixmap(QPixmap(mascot)) # Add the mascot image to the background label.
            
    class StartButton(QPushButton):
        def __init__(
                self,
                parent: QWidget
        ) -> None:
            super().__init__(parent)
            self._add_design()
            
            self.main_window = self.parent().parent()
            
            self.clicked.connect(self._on_click)
        
        def _add_design(self):
            self.setFixedSize(80, 80)
            self.move(10, 20)
            
            # Make the button rounded.
            self.setStyleSheet("border-radius: 30px")
            
            self.set_to_start()
        
        def set_to_start(self):
            self.setIcon(QIcon(path("resources/window/assets/buttons/start.png")))
            self.setIconSize(QSize(
                self.parentWidget().width() - 50,
                self.parentWidget().height() - 50
            ))
        
        def set_to_stop(self):
            self.setIcon(QIcon(path("resources/window/assets/buttons/stop.png")))
            self.setIconSize(QSize(
                self.parentWidget().width() - 50,
                self.parentWidget().height() - 50
            ))
        
        def _save_history(self, links: list[str]):
            """A function to write the links to the history.json file."""
            with open("data/history.json", "r+", encoding = "utf-8") as file:
                data = json.load(file) # Get the current data in the json.
                data["links"] = links # Set the dictionary links to have the new list.
                
                # Move the pointer back to beginning.
                file.seek(0)
                
                # Remove any data left over.
                file.truncate()
                
                json.dump(data, file, indent = 4) # Dump the editted data to the json file.

        def _on_click(self):
            def check_output_directory() -> bool:
                """A function that will check an output directory - returning False if it failed.

                Returns:
                    bool: True | False - whether the check failed: False, or passed: True.
                """
                output_dir = self.main_window.output_directory.text_edit.text()
                
                if not output_dir: # If no output directory is selected.
                    self.main_window.terminal.add_text(f"Output directory not selected.")
                    
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
                        self.main_window.terminal.add_text(f"{output_dir} is invalid.")
                        
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
                
                link_file_dir = self.main_window.file_input.text_edit.text()
                link_inputs = self.main_window.link_input.text_edit.toPlainText()
                
                if not link_file_dir: # If no links file provided.
                    if not link_inputs: # If there's no links in the text box.
                        # This means the user has not added ANY links.
                        message = QMessageBox(self)
                        message.setIcon(QMessageBox.Icon.Critical)
                        message.setWindowTitle("No Links Added")
                        message.setText("You need to input links of creators to be downloaded.")
                        message.setStandardButtons(QMessageBox.StandardButton.Ok)
                        
                        message.exec_() # Execute message box.

                        self.main_window.terminal.add_text("NO LINKS | No links found.")

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
                with open(self.main_window.file_input.text_edit.text(), "r", encoding = "utf-8") as file:
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
                        self.main_window.terminal.add_text(f"LINK FOUND | {link} in {self.main_window.file_input.text_edit.text()}") # Add the finding to terminal.
                
                # If there's links from the text edit.
                if len(link_inputs) > 0:
                    for link in link_inputs:
                        self.main_window.terminal.add_text(f"LINK FOUND | {link}")
            
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
                        
                        self.main_window.terminal.add_text(f"VALID LINK | {link}")
                    
                    else:
                        self.main_window.terminal.add_text(f"INVALID LINK | {link}")
                
                return fixed_links
            
            # Check if the download worker is already running or not.
            try:
                if self.main_window.download_worker is not None:
                    # Disable the start button until the download worker is fully closed.
                    self.setEnabled(False)
                    
                    self.main_window.download_worker.stop() # Stop it if it's a valid attribute.

                    return # Stop processes.
                            
            except AttributeError: # This means that the downloader isn't present.
                pass
            
            if check_output_directory() is False: return
            if check_inputted_links() is False: return
            
            self.main_window.terminal.add_text("Starting processes...")
            
            links = [link.strip() for link in self.main_window.link_input.text_edit.toPlainText().split(",")] # Get a list of items given in link input.
            links_from_file = []
            
            # Read the links in the file input.
            if self.main_window.file_input.text_edit.text(): # If there's a file wanting to be parsed.
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

                self.main_window.terminal.add_text("NO LINKS | No links found.")
                
                return
            
            # Set start button to a stop button icon.
            self.set_to_stop()
            
            self._save_history(links) # Save links to history.json file.
            self.main_window.start_downloader(list(set(links))) # Remove duplicate links.