from src.imports import *

class Updater(QWidget):
    def __init__(self):
        super().__init__()
        self.latest_version = self.get_latest_version()
        self.current_version = self.get_current_version()
        
        self.fonts = Fonts()

        self._add_design()
        self.button = self.Button(self)
    
    def get_latest_version(self) -> float:
        url = "https://api.github.com/repos/N4GR/Coomer-Downloader/releases/latest"
        
        with requests.get(url) as response:
            if response.status_code == 200:
                release = response.json()
                tag : str = release["tag_name"]
                
                version = float(tag.replace("v", ""))
                
                return version
    
    def get_current_version(self) -> float:
        with open(path("resources/version.yaml"), mode = "r", encoding = "utf-8") as file:
            return yaml.safe_load(file)["Version"]
    
    def _get_font(self) -> QFont:
        font = self.fonts.caskaydia.bold
        font.setPointSize(12) # Set size to 10.
        font.setStyleHint(QFont.StyleHint.Monospace)
        
        return font
    
    def _add_design(self):
        self.setFixedSize(300, 300)
        self.setWindowTitle("Version Outdated")
        self.setWindowIcon(QIcon(path("resources/window/assets/window/icon.png")))
        
        text_label = QLabel(parent = self)
        text_label.setText(f"<b>You're running an outdated version of Coomer-Downloader!</b><br><br><br>Current Version<br><font size='2'>v{self.current_version}</font><br><br>Latest Version<br><font size='2'>v{self.latest_version}</font>")
        text_label.setFixedSize(300, 200)
        text_label.setFont(self._get_font())
        text_label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignCenter)
        text_label.setWordWrap(True)
    
    class Button(QPushButton):
        def __init__(self, parent: QWidget):
            super().__init__(parent)
            self._add_design()
            self.url = QUrl("https://github.com/N4GR/Coomer-Downloader/releases/latest")
            
            self.clicked.connect(self._on_click)
        
        def _add_design(self):
            self.setFixedSize(100, 50)
            
            x_centre = (self.parentWidget().width() / 2) - (self.width() / 2) # X Centre with button alignment.
            
            self.move(x_centre, 225)
            
            self.setText("LATEST")
        
        def _on_click(self):
            QDesktopServices.openUrl(self.url) # Open the latest version in browser.
            