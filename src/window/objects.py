# Should be able to run on its own.
from PySide6.QtGui import QFont, QFontDatabase
from src.funcs import path

class Fonts:
    def __init__(self):
        self.caskaydia = self.Caskaydia()
    
    class Caskaydia:
        def __init__(self):
            self.bold = self._load_font(path("resources/window/fonts/CaskaydiaCoveNerdFontMono-Bold.ttf"))
            self.light = self._load_font(path("resources/window/fonts/CaskaydiaCoveNerdFontMono-Light.ttf"))
            self.regular = self._load_font(path("resources/window/fonts/CaskaydiaCoveNerdFontMono-Regular.ttf"))
            self.semi_bod = self._load_font(path("resources/window/fonts/CaskaydiaCoveNerdFontMono-SemiBold.ttf"))
        
        def _load_font(self, dir: str) -> QFont:
            font_id = QFontDatabase.addApplicationFont(dir)
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            
            return QFont(font_family)