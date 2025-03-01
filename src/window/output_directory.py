from src.window.imports import *

# Local imports.
from src.shared.funcs import path

class OutputDirectory(QWidget):
    def __init__(
            self,
            parent: QWidget
    ) -> None:
        super().__init__(parent)
        
        # Setting design of widget.
        self._add_design()
        
        # Getting widget modules.
        self._add_modules()
    
    def _add_design(self):
        self.setFixedSize(700, 75)
        self.move(100, 175)
    
    def _add_modules(self):
        self.button = self.Button(self)
        self.label = self.Label(self)
        self.text_edit = self.TextEdit(self)
    
    class Button(QPushButton):
        def __init__(
                self,
                parent: QWidget
        ) -> None:
            super().__init__(parent)
            # Setting design of widget.
            self._add_design()

        def _add_design(self):
            self.setFixedSize(25, 25)
            self.move(0, 25)
            
            # Set icon of start button.
            self.setIcon(QIcon(path("data/window/assets/buttons/output.png")))
            self.setIconSize(QSize(
                self.width() - 10,
                self.height() - 10
            ))
    
    class Label(QLabel):
        def __init__(
                self,
                parent: QWidget
        ) -> None:
            super().__init__(parent)
            # Setting design of widget.
            self._add_design()

        def _add_design(self):
            self.setFixedSize(200, 25)
            self.move(10, 0)
            
            self.setText("Output Directory:")
    
    class TextEdit(QLineEdit):
        def __init__(
                self,
                parent: QWidget
        ) -> None:
            super().__init__(parent)
            # Setting design of widget.
            self._add_design()

            # Add TextEdit attributes to the widget.
            self._add_attributes()

        def _add_design(self):
            self.setFixedSize(675, 25)
            self.setPlaceholderText("Output directory...")
            
            self.move(25, 25)
        
        def _add_attributes(self):
            self.setReadOnly(True) # Input not allowed.