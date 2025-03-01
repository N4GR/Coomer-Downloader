from src.window.imports import * 

class Terminal(QPlainTextEdit):
    def __init__(
            self,
            parent: QWidget
    ) -> None:
        super().__init__(parent)
        # Set arguments for widget.
        self._set_args()
        
        # Add design to widget.
        self._add_design()
        
        self.add_text("Terminal window launched...")
    
    def _set_args(self) -> None:
        """A function to set the appropriate config for the QPlainTextEdit"""
        self.setReadOnly(True)
        self.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
    
    def _add_design(self) -> None:
        font = QFont("Courier New", 10)
        font.setStyleHint(QFont.StyleHint.Monospace)
        
        self.setFont(font)
        self.setStyleSheet(
            f"background-color: rgb(0, 0, 0);" # Background colour.
            f"color: rgb(49, 255, 0);" # Font colour.
        )
    
        self.setFixedSize(700, 300) # Setting fixed size.
        
        self.move(100, 300)
    
    def add_text(
            self,
            text: str
    ) -> None:
        now = datetime.now()
        formatted_time = now.strftime("%H:%M:%S") + f".{now.microsecond // 10000:02d}" # Microseconds to 2 decimal places.
        
        self.appendPlainText(f"{formatted_time} | {text}") # Add text to new line with formatted date.