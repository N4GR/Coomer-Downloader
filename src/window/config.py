from src.window.imports import *

class Widget:
    def __init__(
            self,
            height: int,
            width: int,
            x: int,
            y: int
    ) -> None:
        self.height = height
        self.width = width
        self.x = x
        self.y = y

class Config:
    class LinkInput:
        def __init__(self):
            self.widget = Widget(
                height = 100,
                width = 700,
                x = 100,
                y = 0
            )
            
            self.label = self.Label()
            
        class Label:
            def __init__(self):
                self.widget = Widget(
                    height = 25,
                    width = 250,
                    x = 10,
                    y = 0
                )