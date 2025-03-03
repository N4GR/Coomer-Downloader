from src.imports import *

class OutputDirectory(QWidget):
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
        self.move(450, 100)
    
    def _add_modules(self):
        self.button = self.Button(self)
        self.label = self.Label(self, self.fonts)
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
            self.setIcon(QIcon(path("resources/window/assets/buttons/output.png")))
            self.setIconSize(QSize(
                self.width() - 10,
                self.height() - 10
            ))
        
        def _on_click(self):
            dir_name = QFileDialog.getExistingDirectory(self, "Select output directory")
        
            # If the directory is selected, add it to the output_directory text input and log it to terminal.
            if dir_name:
                self.parent().text_edit.setText(dir_name)
                self.main_window.terminal.add_text(f"Set {dir_name} as output directory.")
    
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
            self.setText("Output Directory:")
            self.setFixedSize(200, 25)
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
            self.setPlaceholderText("Output directory...")
            self.setFixedSize(325, 25)
            self.setFont(self._get_font())
            self.move(25, 25)
        
        def _add_attributes(self):
            self.setReadOnly(True) # Input not allowed.