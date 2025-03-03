from src.imports import *

class FileInput(QWidget):
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
        self.setFixedSize(350, 75)
        self.move(100, 100)
    
    def _add_modules(self):
        self.label = self.Label(self, self.fonts)
        self.button = self.Button(self)
        self.text_edit = self.TextEdit(self, self.fonts)

    class Button(QPushButton):
        def __init__(
                self,
                parent: QWidget
        ) -> None:
            super().__init__(parent)
            # Setting design of widget.
            self._add_design()
            
            self.main_window = self.parent().parent()
            
            self.clicked.connect(self._on_click)

        def _add_design(self):
            self.setFixedSize(25, 25)
            self.move(0, 25)
            
            # Set icon of start button.
            self.setIcon(QIcon(path("resources/window/assets/buttons/file.png")))
            self.setIconSize(QSize(
                self.width() - 10,
                self.height() - 10
            ))
        
        def _on_click(self):
            # Open the explorer to retrieve a text file.
            file_path, _ = QFileDialog.getOpenFileName(self, "Select Text File", "", "Text Files (*.txt)")
            
            # If a file is selected, add it to the file_input text and add a terminal log entry.
            if file_path:
                self.parent().text_edit.setText(file_path)
                self.main_window.terminal.add_text(f"Set {file_path} as links document.")
    
    class Label(QLabel):
        def __init__(
                self,
                parent: QWidget,
                fonts: Fonts
        ) -> None:
            super().__init__(parent)
            self.fonts = fonts
            
            # Setting design of widget.
            self._add_design()
        
        def _get_font(self) -> QFont:
            font = self.fonts.caskaydia.bold
            font.setPointSize(10) # Set size to 10.
            font.setStyleHint(QFont.StyleHint.Monospace)
            font.setBold(True)
        
            return font

        def _add_design(self):
            self.setText("Links File Input (optional):")
            self.setFixedSize(250, 25)
            self.setFont(self._get_font())
            self.move(10, 0)
    
    class TextEdit(QLineEdit):
        def __init__(
                self,
                parent: QWidget,
                fonts: Fonts
        ) -> None:
            super().__init__(parent)
            self.fonts = fonts
            
            # Setting design of widget.
            self._add_design()

            # Add TextEdit attributes to the widget.
            self._add_attributes()
        
        def _get_font(self) -> QFont:
            font = self.fonts.caskaydia.bold
            font.setPointSize(8) # Set size to 10.
            font.setStyleHint(QFont.StyleHint.Monospace)
        
            return font

        def _add_design(self):
            self.setPlaceholderText("Links directory...")
            self.setFixedSize(325, 25)
            self.setFont(self._get_font())
            self.move(25, 25)
        
        def _add_attributes(self):
            self.setReadOnly(True) # Input not allowed.