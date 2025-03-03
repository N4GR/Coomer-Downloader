from src.imports import *

# Type-hinting.
from src.window.widgets.terminal import Terminal

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
    
    def _get_socials(self) -> list[dict]:
        with open(path("resources/socials.yaml"), mode = "r", encoding = "utf-8") as file:
            return yaml.safe_load(file)
    
    def _add_widgets(self): 
        social_icon_path = path("resources/window/assets/buttons/socials")
        
        # For every social in the socials data, create a socials button.
        for social in self._get_socials():
            social_widget = self.Social(
                parent = self,
                fonts = self.fonts,
                icon_path = f"{social_icon_path}/{social['icon_file_name']}",
                name = social["name"],
                type = social["type"],
                args = social["args"]
            ) # Create the social object.
            
            # Add the object to the layout.
            self.box_layout.addWidget(social_widget)

    class Social(QWidget):
        def __init__(
                self,
                parent: QWidget,
                fonts: Fonts,
                icon_path: str,
                name: str,
                type: str,
                args: dict
        ):
            super().__init__(parent)

            self.fonts = fonts
            self.icon_path = icon_path
            self.name = name
            self.type = type
            self.args = args
            
            self._add_design()
            
            self.button = self.Button(
                parent = self,
                fonts = self.fonts,
                icon_path = self.icon_path,
                type = self.type,
                args = self.args
            )
        
        def _add_design(self):
            self.setFixedSize(64, 84)
            
            self.label = self.Label(
                parent = self,
                name = self.name,
                fonts = self.fonts
            )
        
        class Button(QPushButton):
            def __init__(
                    self,
                    parent: QWidget,
                    fonts: Fonts,
                    icon_path: str,
                    type: str,
                    args: dict
            ):
                super().__init__(parent)
                self.fonts = fonts
                self.icon_path = icon_path
                self.type = type
                self.args = args
                
                # Terminal inside the main_window.
                self.terminal : Terminal = self.parent().parent().parent().terminal

                self._handle_connection()
                self._add_design()
                
            def _add_design(self):
                self.setFixedSize(64, 64)
                
                icon_size = QSize(32, 32)
                
                self.setIcon(QPixmap(self.icon_path).scaled(icon_size))
                self.setIconSize(icon_size)
            
            def _handle_connection(self):
                def url_click():
                    self.terminal.add_text(f"Opening URL: {url.url()}")
                    
                    QDesktopServices.openUrl(url)
                
                def message_click():
                    self.terminal.add_text(f"Opening Crypto window.")
                    
                    self.message_box = self.MessageBox(
                        fonts = self.fonts,
                        args = self.args,
                        terminal = self.terminal
                    ) # Create the message box object.
                
                    self.message_box.show() # Open the message box.

                if self.type == "link": # Add a link opening function.
                    url = QUrl(self.args["link"])
                    
                    self.clicked.connect(url_click)
                
                elif self.type == "info": # Open a message box on click for info.
                    self.clicked.connect(message_click)
            
            class MessageBox(QWidget):
                def __init__(
                        self,
                        fonts: Fonts,
                        args: list[dict],
                        terminal: Terminal
                ):
                    super().__init__()
                    
                    self.fonts = fonts
                    self.args = args
                    self.terminal = terminal
                    
                    self._add_design()
                    self._add_widgets()
                    
                def _add_design(self):
                    self.setFixedSize(300, 600)
                    
                    self.setWindowTitle("Crypto Addresses")
                    
                    self.box_layout = QVBoxLayout(self)
                    self.box_layout.setSpacing(0)
                    self.box_layout.setContentsMargins(0, 0, 0, 0)
                    
                    self.setLayout(self.box_layout)
                    
                    # Set window icon.
                    self.setWindowIcon(QIcon(path("resources/window/assets/window/icon.png")))
                
                def _add_widgets(self):
                    for wallet in self.args:
                        self.box_layout.addWidget(self.Crypto(
                            fonts = self.fonts,
                            wallet = wallet
                        ))
                
                def closeEvent(self, event: QEvent):
                    self.terminal.add_text("Closing Crypto window.")
                    
                    event.accept()
                
                class Crypto(QWidget):
                    def __init__(self, fonts: Fonts, wallet: dict):
                        super().__init__()
                        self.fonts = fonts
                        self.wallet = wallet
                    
                        self._add_design()
                        self._add_widgets()
                    
                    def _add_design(self):
                        self.setFixedSize(300, 150)
                        
                        self.box_layout = QVBoxLayout() # Stack the items on top of each other.
                        self.setLayout(self.box_layout)
                        self.box_layout.setSpacing(0)
                        self.box_layout.setContentsMargins(0, 0, 0, 0)
                    
                    def _get_font(self, bold: bool, size: int) -> QFont:
                        font = self.fonts.caskaydia.bold
                        font.setPointSize(size) # Set size to 10.
                        font.setStyleHint(QFont.StyleHint.Monospace)
                        font.setBold(bold)
                        
                        return font
                    
                    def _add_widgets(self):
                        self.box_layout.addWidget(self.Label(
                            font = self._get_font(True, 12),
                            label_text = self.wallet["name"]
                        )) # Wallet name label.
                        
                        self.box_layout.addWidget(self.Image(
                            image_dir = self.wallet["icon_file_name"]
                        )) # Wallet icon label.
                        
                        self.box_layout.addWidget(self.Address(
                            font = self._get_font(False, 8),
                            label_text = self.wallet["wallet_address"]
                        )) # Wallet address label.
                    
                    class Image(QLabel):
                        def __init__(self, image_dir: str):
                            super().__init__()
                            self.image_dir = image_dir
                            
                            self._add_design()
                        
                        def _add_design(self):
                            self.setFixedSize(300, 100)
                            self.setStyleSheet("background-color: transparent")
                            
                            crypto_icon_path = path("resources/window/assets/buttons/socials/crypto")
                            icon_path = f"{crypto_icon_path}/{self.image_dir}"
                            self.setAlignment(Qt.AlignmentFlag.AlignCenter)
                            
                            self.setPixmap(QPixmap(icon_path).scaled(100, 100))
                            
                    class Label(QLabel):
                        def __init__(
                                self,
                                font: QFont,
                                label_text: str
                        ):
                            super().__init__()
                            self.label_font = font
                            self.label_text = label_text
                        
                            self._add_design()
                        
                        def _add_design(self):
                            self.setFixedSize(300, 20)
                            self.setText(self.label_text)
                            self.setStyleSheet("background-color: transparent")
                            
                            self.setAlignment(Qt.AlignmentFlag.AlignCenter)
                            
                            self.setFont(self.label_font)
                    
                    class Address(QTextEdit):
                        def __init__(self, font: QFont, label_text: str):
                            super().__init__()
                            self.label_font = font
                            self.label_text = label_text
                        
                            self._add_design()
                        
                        def _add_design(self):
                            self.setFixedSize(300, 20)
                            self.setText(self.label_text)
                            self.setReadOnly(True)
                            self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
                            self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
                            self.setStyleSheet("background-color: transparent; border: none;")
                            
                            self.setAlignment(Qt.AlignmentFlag.AlignCenter)
                            
                            self.setFont(self.label_font)
                    
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
            
            def _get_font(self) -> QFont:
                font = self.fonts.caskaydia.bold
                font.setPointSize(12) # Set size to 10.
                font.setStyleHint(QFont.StyleHint.Monospace)
                font.setBold(True)
            
                return font
            
            def _add_design(self):
                self.setFixedSize(64, 20)
                
                self.setText(self.name)
                self.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
                self.move(0, 64)
                
                self.setStyleSheet("background-color: transparent")
                
                self.setFont(self._get_font())