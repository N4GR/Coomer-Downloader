from src.imports import QApplication
from src.window.main_window import MainWindow

from src.updater import Updater

class Main:
    def __init__(
            self,
            launch_args: list[str]
    ) -> None:
        # If the program was launched with --cli arg, run in CLI instead of with window.
        if self.in_cli(launch_args) is True:
            self.run_cli()
        else:
            self.run_window() # Run in window mode if program was launched without --cli argument.
    
    def in_cli(
        self,
        launch_args: list[str]
    ) -> bool:
        """A function to check if the program was launched with the "--cli" argument to launch the window or not.

        Args:
            launch_args (list[str]): A list of strings that were parsed on launch.

        Returns:
            bool: True | False - whether the program was launched with --cli flag or not.
        """
        cli_arg = "--cli"
        
        if cli_arg in launch_args:
            return True
        else:
            return False
    
    def run_cli(self):
        """A function that will run the CLI if the --clie argument appears in launch variables."""
        print("Running the program in CLI mode...")
    
    def run_window(self):
        """A function that will run the window if the --cli argument is missing from launch variables."""
        print("Running in window mode.")
        
        self.application = QApplication([]) # Create the application for PySide6.
        
        self.main_window = MainWindow() # Create main window object.
        self.main_window.show() # Show the main window.
        
        self.updater = Updater() # Check the updater for latest version.
        
        if self.updater.current_version < self.updater.latest_version:
            self.updater.show() # Show the updater if the version is out of date.
        
        else:
            # Destroy widget.
            self.updater = None
        
        self.application.exec_() # Execute PySide6 event loop.