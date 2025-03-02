from src.window.imports import *

from src.window.objects import Fonts

class LinkInput(QWidget):
    def __init__(
            self,
            parent: QWidget
    ) -> None:
        super().__init__(parent)
        self.fonts = Fonts()
        
        # Setting design of widget.
        self._add_design()
        
        # Getting widget modules.
        self._add_modules()
    
    def _add_design(self):
        self.setFixedSize(700, 100)
        self.move(100, 0)
    
    def _add_modules(self):
        self.label = self.Label(self, self.fonts)
        self.text_edit = self.TextEdit(self, self.fonts)
    
    class Label(QLabel):
        def __init__(
                self,
                parent: QWidget,
                fonts: Fonts
        ) -> None:
            super().__init__(parent)
            self.fonts = fonts
            
            # Adding design to widget.
            self._add_design()
        
        def _get_font(self) -> QFont:
            font = self.fonts.caskaydia.bold
            font.setPointSize(10) # Set size to 10.
            font.setStyleHint(QFont.StyleHint.Monospace)
            font.setBold(True)
        
            return font
        
        def _add_design(self):
            self.setText("Links Input (optional):") # Add label text.
            self.setFixedSize(250, 25)
            self.setFont(self._get_font())
            self.move(10, 0) # Move to top left of widget.
    
    class TextEdit(QTextEdit):
        def __init__(
                self,
                parent: QWidget,
                fonts: Fonts
        ) -> None:
            super().__init__(parent)
            self.fonts = fonts
            
            # Adding design to widget.
            self._add_design()
            
            self._add_attributes()
        
        def _get_font(self) -> QFont:
            font = self.fonts.caskaydia.bold
            font.setPointSize(8) # Set size to 10.
            font.setStyleHint(QFont.StyleHint.Monospace)
        
            return font
        
        def _add_design(self):
            self.setPlaceholderText("Add links seperated by a ','")
            self.setFixedSize(700, 75)
            self.setFont(self._get_font())
            self.move(0, 25)
        
        def _add_attributes(self):
            self.setAcceptRichText(False)