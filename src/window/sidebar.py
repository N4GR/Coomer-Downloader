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

            # Select a random mascot from the provided images.
            mascot = random.choice([
                path("data/window/assets/window/mascots/") + mascot
                for mascot
                in os.listdir(path("data/window/assets/window/mascots"))
            ])
            
            self.setPixmap(QPixmap(mascot)) # Add the mascot image to the background label.
            
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
            
            self.set_to_start()
        
        def set_to_start(self):
            self.setIcon(QIcon(path("data/window/assets/buttons/start.png")))
            self.setIconSize(QSize(
                self.parentWidget().width() - 50,
                self.parentWidget().height() - 50
            ))
        
        def set_to_stop(self):
            self.setIcon(QIcon(path("data/window/assets/buttons/stop.png")))
            self.setIconSize(QSize(
                self.parentWidget().width() - 50,
                self.parentWidget().height() - 50
            ))