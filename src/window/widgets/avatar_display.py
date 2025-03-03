from src.imports import *

# Local imports.
from src.network.downloader import get_pixmap_from_url

class AvatarDisplay(QWidget):
    def __init__(
            self,
            parent: QWidget
    ) -> None:
        super().__init__(parent)
        self.fonts = Fonts()
        
        self._add_design()
    
        # Add widgets to the scroll area.
        self._add_widgets()
        
        self.lock = threading.Lock() # For save adding to numbers.
        
        self.row = 0 # Keep track of rows.
        self.col = 0 # Keep track of columns.
        self.max_col = 5 # Maximum amount of columns.
        
    def _add_design(self):
        self.setFixedSize(700, 300)
        self.move(800, 0)
    
    def _add_widgets(self):
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        
        self.content = QWidget(self.scroll_area)
        
        self.grid_layout = QGridLayout(self.content)
        self.grid_layout.setHorizontalSpacing(10)
        self.grid_layout.setVerticalSpacing(10)
        
        self.content.setLayout(self.grid_layout)
        self.scroll_area.setWidget(self.content)
        
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.scroll_area)
        
        self.setLayout(main_layout)
    
    def add_avatar(
            self,
            profile: Profile
    ) -> None:
        with self.lock: # Add numbers with lock, for thread-safe operation.
            if self.col % self.max_col == 0: # If current column is a multiple of max_col, reset col to 0.
                self.row += 1
                self.col = 0
        
        avatar = Avatar(profile, self.fonts)
        self.grid_layout.addWidget(avatar, self.row, self.col)
        
        # Add 1 to column.
        self.col += 1

    def reset_values(self):
        """A function to reset all values once the avatars are deleted."""
        self.row = 0
        self.col = 0
    
    def reset_display(self):
        """A function that will reset the avatar display, removing any present avatars."""
        self.row = 0
        self.col = 0
        
        # Iterate over items in avatar display and delete the avatars.
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            
            if item.widget():
                item.widget().deleteLater() # Delete widget.
    
    def set_avatar_file_count(
        self,
        file_data: dict
    ) -> None:
        completed_files = file_data["files_complete"]
        file_count = file_data["file_count"]
        row = file_data["row"]
        col = file_data["column"]
        
        avatar_item = self.grid_layout.itemAtPosition(row, col)
        avatar : Avatar = avatar_item.widget()
        
        # Set the text for the count label.
        avatar.file_count_label.setText(f"{completed_files}/{file_count}")
        
        if avatar.file_count_label.isHidden(): # Unhide the count label if hidden.
            avatar.file_count_label.setHidden(False)
    
class Avatar(QWidget):
    def __init__(
            self,
            profile: Profile,
            fonts: Fonts
    ) -> None:
        super().__init__()
        self.fonts = fonts
        
        self.profile = profile
        
        self._add_design()
        self._add_widgets()
    
    def _add_design(self):
        self.setFixedSize(100, 130)
    
    def _add_widgets(self):
        self.image = self.Image(self, self.profile)
        self.text_label = self.TextLabel(self, self.profile, self.fonts)
        self.file_count_label = self.FileCount(self, self.fonts)
    
    class Image(QLabel):
        def __init__(
                self,
                parent: QWidget,
                profile: Profile
        ) -> None:
            super().__init__(parent)
            self.profile = profile
            
            self._add_design()
        
        def _add_design(self):
            self.setStyleSheet("background-color: white;")
            self.setFixedSize(100, 100)
            self.move(0, 15) # Move it down 25px for the file count.
            
            pixmap = get_pixmap_from_url(self.profile.image).scaled(self.size()) # Get the profile image and resize it to fit image label.
            
            self.setPixmap(pixmap)
    
    class TextLabel(QLabel):
        def __init__(
                self,
                parent: QWidget,
                profile: Profile,
                fonts: Fonts
        ) -> None:
            super().__init__(parent)
            self.profile = profile
            self.fonts = fonts
            
            self._add_design()
        
        def _get_font(self) -> QFont:
            font = self.fonts.caskaydia.bold
            font.setPointSize(8) # Set size to 10.
            font.setStyleHint(QFont.StyleHint.Monospace)
            font.setBold(True)
        
            return font
        
        def _add_design(self):
            self.setText(self.profile.name.capitalize()) # Set the avatar label to the username.
            self.setAlignment(Qt.AlignmentFlag.AlignCenter) # Align the text to the centre.
            self.setFixedSize(100, 15) # Set a fixed size for the label.
            self.setFont(self._get_font())
            self.move(0, 117) # Move the label below the image.
    
    class FileCount(QLabel):
        def __init__(
                self,
                parent: QWidget,
                fonts: Fonts
        ) -> None:
            super().__init__(parent)
            self.fonts = fonts
            
            self._add_design()
        
        def _get_font(self) -> QFont:
            font = self.fonts.caskaydia.light
            font.setPointSize(8) # Set size to 10.
            font.setStyleHint(QFont.StyleHint.Monospace)
        
            return font
        
        def _add_design(self):
            self.setText("0/0") # File placeholder.
            self.setFixedSize(self.parentWidget().width(), 25) # Fill width, but not height.
            self.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop) # Align to right of avatar.
            
            # Hide background of file count, so avatar can be displayed behind.
            self.setStyleSheet("background-color: transparent;")
            
            self.setFont(self._get_font())
            
            self.setHidden(True) # Hide it at first, only display on text change.