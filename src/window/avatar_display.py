from src.window.imports import *

class AvatarDisplay(QWidget):
    def __init__(
            self,
            parent: QWidget
    ) -> None:
        super().__init__(parent)
        self._add_design()
    
        # Add widgets to the scroll area.
        self._add_widgets()
        
    def _add_design(self):
        self.setFixedSize(700, 300)
        self.move(800, 0)
        
        label = QLabel(self)
        label.setFixedSize(self.size())
        label.setStyleSheet("background-color: red; border: 2px solid white")
    
    def _add_widgets(self):
        self.scroll_area = self.ScrollArea(self)
        self.content = self.Content(self.scroll_area)
        self.grid_layout = self.GridLayout(self.content)
        
        self.add_avatar()
    
    def add_avatar(self):
        for row in range(10):
            for col in range(10):
                avatar = self.Avatar()
                
                self.grid_layout.addWidget(avatar, row, col)
    
    class ScrollArea(QScrollArea):
        def __init__(
                self,
                parent: QWidget
        ) -> None:
            super().__init__(parent)
            self._add_design()
    
        def _add_design(self):
            self.setFixedSize(self.parentWidget().size())
            
            self.setStyleSheet("background-color: transparent;")
    
    class Content(QWidget):
        def __init__(
                self,
                parent: QScrollArea
        ) -> None:
            super().__init__(parent)
            self._add_design()
    
        def _add_design(self):
            self.setFixedSize(self.parentWidget().size())
            
            self.setStyleSheet("background-color: transparent;")
    
    class GridLayout(QGridLayout):
        def __init__(
                self,
                parent: QWidget
        ) -> None:
            super().__init__(parent)
            self._add_design()
    
        def _add_design(self):
            pass
    
    class Avatar(QWidget):
        def __init__(self) -> None:
            super().__init__()
            self._add_design()
            self._add_widgets()
        
        def _add_design(self):
            self.setFixedSize(125, 125)
        
        def _add_widgets(self):
            self.image = self.Image(self)
            self.label = self.Label(self)
        
        class Image(QLabel):
            def __init__(
                    self,
                    parent: QWidget
            ) -> None:
                super().__init__(parent)
        
        class Label(QLabel):
            def __init__(
                    self,
                    parent: QWidget
            ) -> None:
                super().__init__(parent)
                self._add_design()
            
            def _add_design(self):
                pass