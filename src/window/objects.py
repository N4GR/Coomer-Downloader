from src.window.imports import *
from src.shared.funcs import path

class Fonts:
    def __init__(self):
        self.caskaydia = self.Caskaydia()
    
    class Caskaydia:
        def __init__(self):
            self.bold = self._load_font(path("data/window/fonts/CaskaydiaCoveNerdFontMono-Bold.ttf"))
            self.light = self._load_font(path("data/window/fonts/CaskaydiaCoveNerdFontMono-Light.ttf"))
            self.regular = self._load_font(path("data/window/fonts/CaskaydiaCoveNerdFontMono-Regular.ttf"))
            self.semi_bod = self._load_font(path("data/window/fonts/CaskaydiaCoveNerdFontMono-SemiBold.ttf"))
        
        def _load_font(self, dir: str) -> QFont:
            font_id = QFontDatabase.addApplicationFont(dir)
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            
            return QFont(font_family)