from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from tetris import Tetris

class TetrisWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tetris = Tetris()
        
    def update(self, dt):
        self.tetris.run()

class TetrisApp(App):
    def build(self):
        game = TetrisWidget()
        return game

if __name__ == '__main__':
    TetrisApp().run() 