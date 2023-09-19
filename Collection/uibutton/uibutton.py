from kivy.uix.floatlayout import FloatLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import NumericProperty,ColorProperty, StringProperty, BooleanProperty, ColorProperty, ListProperty
from kivy.animation import Animation
from kivy.clock import Clock
from Collection.uitouchripple.uitouchripple import UITouchRipple
from kivymd.uix.behaviors import RectangularRippleBehavior

class UIButton(ButtonBehavior, RectangularRippleBehavior, FloatLayout):

    text  = StringProperty("")
    text_color = StringProperty("fff")
    bg_color   = ColorProperty([1,1,1,0])
    radius     = ListProperty([0,0,0,0])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        

        