import os
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.utils import get_color_from_hex
from kivy.uix.button import Button
from kivy.animation import Animation
import requests

# Cargamos el archivo kv
with open(os.path.join(os.getcwd(), "screens", "kv", "home.kv"), encoding="utf-8") as KV:
    Builder.load_string(KV.read())


# Botón para mostrar y ocultar el listado de criptos
class SwipeButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Asignamos un listener para conocer cuando el usuario intenta arrastrar nuestro botón
        self.bind(on_touch_move=self._on_swipe)
    
    '''
    Método para cambiar la altura del componente `RoundedBoxLayout` con 
    respecto a la dirección en que se arrastra el botón SwipeButton
    '''
    def _on_swipe(self, instance, touch):
        # La altura máxima de `RoundedBoxLayout` será de 370dp
        # y la altura mínima será 50dp
        if touch.y > 50 and touch.y < 370:
            # Se asigna la dirección en que se arrastra como altura del componente padre del botón (`RoundedBoxLayout`)
            self.parent.height = touch.y

    '''
    Método para identificar el momento en que se deja de precionar el botón.
    Esto nos servira para decidir si lo ocultamos o lo abrimos el componente `RoundedBoxLayout` por completo
    '''
    def on_state(self, instance, state):
        # Si el botón es soltado y llega a su estado "normal"
        if state == "normal":
            # Si la altura de `RoundedBoxLayout` es menor a 200 dp cerraremos el componente
            if instance.parent.height <= 200:
                # Animación para cerrar el componente con una duracion de 1/2 segundo
                anim = Animation(height=50, duration=.5)
                anim.start(instance.parent)

            # Si la altura de `RoundedBoxLayout` es mayor a 200 dp abriremos el componente
            else:
                # Animación para abrir el componente con una duracion de 1/2 segundo
                anim = Animation(height=370, duration=.5)
                anim.start(instance.parent)


# BoxLayout con las orillas redondeadas (Su estilo se define en el archivo kv)
class RoundedBoxLayout(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

# Items para la lista de criptomonedas (Su estilo se define en el archivo kv)
class CryptoItemList(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.negative_color = get_color_from_hex("#FF3333")
        self.positive_color = get_color_from_hex("#2DAC29")


# Pantalla donde se plasmarán los componentes de la pantalla
class HomeScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._load_cryptos()

    '''
    Método para consultar la información de las criptos por medio de la API https://docs.coincap.io/
    Las imagenes de las criptomonedas son consultadas desde el siguiente proyecto de GitHub https://github.com/ErikThiart/cryptocurrency-icons
    '''
    def _load_cryptos(self):
        # URL para obtener las primeras 30 criptomonedas de la API
        URL     = 'https://api.coincap.io/v2/assets/?limit=30&?offset=0'
        # Por medio de la libreria requests obtenemos el resultado y lo transformamos a JSON
        cryptos = requests.get(URL).json()['data']

        # Recorremos las criptos obtenidas de la consulta y generamos los items para el listado
        for crypto in cryptos:
            item_list                    = CryptoItemList()
            item_list.source             = f"https://raw.githubusercontent.com/ErikThiart/cryptocurrency-icons/master/32/{crypto['id']}.png"
            item_list.name               = crypto['name']
            item_list.price              = "${:,.2f}".format(float(crypto['priceUsd']))
            item_list.changePercent      = "{:,.2f}%".format(float(crypto['changePercent24Hr']))
            item_list.changePercentColor = item_list.negative_color if str(item_list.changePercent).startswith("-") else item_list.positive_color

            # Agregamos la nueva cripto a la lista
            self.ids.crypto_list.add_widget(item_list)
