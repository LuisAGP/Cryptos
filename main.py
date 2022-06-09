from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from screens.py import home
from kivymd.color_definitions import colors
from kivy.utils import get_color_from_hex

class Wallet(MDApp):
    def build(self):
        # Colores para la aplicación
        self.theme_cls.primary_palette = 'Orange'
        self.bg_color = get_color_from_hex(colors['Orange']['300'])
        self.text_color = get_color_from_hex("#112A46")

        self.sm = ScreenManager()
        self.sm.add_widget(home.HomeScreen())

        return self.sm

if __name__=="__main__":
    Wallet().run()