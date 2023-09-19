from kivy.uix.widget import Widget
from kivy.properties import (
    NumericProperty,
    ColorProperty, 
    StringProperty, 
    BooleanProperty, 
    ColorProperty, 
    ListProperty)
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.graphics import (
    Color,
    Ellipse,
    StencilPop,
    StencilPush,
    StencilUnUse,
    StencilUse,
)
from kivy.graphics.vertex_instructions import RoundedRectangle
from kivy.uix.stencilview import StencilView

class UITouchRipple(StencilView, Widget):

    _sizer  = ListProperty([5,5])
    _poser  = ListProperty([0,0])

    sizer  = ListProperty([5,5])
    poser  = ListProperty([0,0])

    _color = ColorProperty([0,0,0,0])
    color = ColorProperty([1,1,0,0.3])

    _radius = ListProperty([5,5,5,5])
    

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        

    def on_touch_down(self, touch):
        
        if self.collide_point(touch.x, touch.y):
            touch.grab(self)

            self.sizer = [15,15]
            self.poser = (touch.x - self.sizer[0]/2, touch.y - self.sizer[1]/2)

            self._sizer = [self.width, self.width]
            self._poser = [self.x, self.y]

            anim = Animation(
                sizer=self._sizer,
                poser=self._poser, 
                color=self.color,
                d=0.2)
            anim += Animation(
                color=self.color,
                d=0.05)
            anim.start(self)
            

        return super().on_touch_down(touch)
    
    def on_touch_move(self, touch):
        if self.collide_point(touch.x, touch.y):
            pass
        return super().on_touch_move(touch)
    
    def on_touch_up(self, touch):
        if touch.grab_current is self:
            touch.ungrab(self)

        return super().on_touch_up(touch)

    def remove_ripple(self, *args):
        self.canvas.remove_group("touchripple")

        self._sizer = [5,5]