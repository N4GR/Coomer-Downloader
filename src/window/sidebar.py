from src.window.imports import *

# Local imports.
from src.shared.funcs import path

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

            self.setPixmap(QPixmap("data/window/assets/window/mascot.png")) # Add the mascot image to the background label.
            
    class StartButton(QPushButton):
        def __init__(
                self,
                parent: QWidget
        ) -> None:
            super().__init__(parent)
            self._add_design()
        
        def _add_design(self):
            self.setFixedSize(80, 80)
            self.move(10, 20)
            
            # Make the button rounded.
            self.setStyleSheet("border-radius: 30px")
            
            # Set icon of start button.
            self.setIcon(QIcon(path("data/window/assets/buttons/start.png")))
            self.setIconSize(QSize(
                self.parentWidget().width() - 50,
                self.parentWidget().height() - 50
            ))