from src.window.imports import *

class LinkInput(QWidget):
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
        self.setFixedSize(700, 100)
        self.move(100, 0)
    
    def _add_modules(self):
        self.label = self.Label(self)
        self.text_edit = self.TextEdit(self)
    
    class TextEdit(QTextEdit):
        def __init__(
                self,
                parent: QWidget
        ) -> None:
            super().__init__(parent)
            # Adding design to widget.
            self._add_design()
        
        def _add_design(self):
            self.setPlaceholderText("Add links seperated by a ','")
            self.setAcceptRichText(False)
            
            self.setFixedSize(700, 75)
            
            self.move(0, 25)
    
    class Label(QLabel):
        def __init__(
                self,
                parent: QWidget
        ) -> None:
            super().__init__(parent)
            # Adding design to widget.
            self._add_design()
        
        def _add_design(self):
            self.setText("Links Input (optional):") # Add label text.
            self.move(10, 0) # Move to top left of widget.
            
            self.setFixedSize(200, 25)