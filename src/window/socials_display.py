from src.window.imports import *
from src.shared.imports import *
from src.shared.funcs import path
from src.window.objects import Fonts

class SocialsDisplay(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.fonts = Fonts()
        
        self._add_design()
        self._add_widgets()
    
    def _add_design(self):
        self.setFixedSize(680, 130)
        
        self.move(110, 160)
        
        self.box_layout = QHBoxLayout(self)
        self.box_layout.setSpacing(10)
        
        self.setLayout(self.box_layout)
    
    def _add_widgets(self):
        def _add_to_grid():
            self.box_layout.addWidget(self.discord)
            self.box_layout.addWidget(self.github)
            self.box_layout.addWidget(self.kofi)
            self.box_layout.addWidget(self.youtube)
        
        self.discord = self.Social(
            parent = self,
            fonts = self.fonts,
            icon_path = path("data/window/assets/buttons/socials/discord.png"),
            name = "Discord",
            link = "https://n4gr.uk/discord",
        )
        
        self.github = self.Social(
            parent = self,
            fonts = self.fonts,
            icon_path = path("data/window/assets/buttons/socials/github.png"),
            name = "GitHub",
            link = "https://n4gr.uk/github"
        )
        
        self.kofi = self.Social(
            parent = self,
            fonts = self.fonts,
            icon_path = path("data/window/assets/buttons/socials/kofi.png"),
            name = "KoFi",
            link = "https://n4gr.uk/ko-fi"
        )
        
        self.youtube = self.Social(
            parent = self,
            fonts = self.fonts,
            icon_path = path("data/window/assets/buttons/socials/youtube.png"),
            name = "YouTube",
            link = "https://n4gr.uk/youtube"
        )
        
        _add_to_grid()
    
    class Social(QWidget):
        def __init__(
                self,
                parent: QWidget,
                fonts: Fonts,
                icon_path: str,
                name: str,
                link: str
        ):
            super().__init__(parent)

            self.fonts = fonts
            self.icon_path = icon_path
            self.name = name
            self.link = link
            
            self._add_design()
            self._add_widgets()
        
        def _add_design(self):
            self.setFixedSize(64, 84)
        
        def _add_widgets(self):
            self.button = self.Button(
                parent = self,
                icon_path = self.icon_path,
                link = self.link
            )
            
            self.label = self.Label(
                parent = self,
                name = self.name,
                fonts = self.fonts
            )
        
        class Button(QPushButton):
            def __init__(
                    self,
                    parent: QWidget,
                    icon_path: str,
                    link: str
            ):
                super().__init__(parent)
                self.icon_path = icon_path
                self.link = QUrl(link)
                
                self._add_design()
                self._add_connections()
                
            def _add_design(self):
                self.setFixedSize(64, 64)
                
                icon_size = QSize(32, 32)
                
                self.setIcon(QPixmap(self.icon_path).scaled(icon_size))
                self.setIconSize(icon_size)
            
            def _add_connections(self):
                self.clicked.connect(self._on_click)
            
            def _on_click(self):
                QDesktopServices.openUrl(self.link)
        
        class Label(QLabel):
            def __init__(
                    self,
                    parent: QWidget,
                    fonts: Fonts,
                    name: str
            ):
                super().__init__(parent)
                self.name = name
                self.fonts = fonts
                
                self._add_design()
            
            def _add_design(self):
                self.setFixedSize(64, 20)
                
                self.setText(self.name)
                self.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
                self.move(0, 64)
                
                self.setStyleSheet("background-color: transparent")
                
                self.setFont(self._get_font())
            
            def _get_font(self) -> QFont:
                font = self.fonts.caskaydia.bold
                font.setPointSize(12) # Set size to 10.
                font.setStyleHint(QFont.StyleHint.Monospace)
                font.setBold(True)
            
                return font