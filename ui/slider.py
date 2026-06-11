import pygame as pg
class Slider:
    def __init__(self, x,y,width,min_value,max_value,step=1,initial=None,label='',value_to_text=None):
        self.track_rect = pg.Rect(x,y,width,30)
        self.handle_radius = 10
        self.min = float(min_value)
        self.max = float(max_value)
        self.step = float(step)
        if initial is not None:
            self.value = float(initial)
        else:            
            self.value = self.min
        self.label = label
        self.value_to_text = value_to_text
        self.dragging = False

        self._hit_rect = pg.Rect(0,0,self.handle_radius*2+8,self.handle_radius*2+8)
    def _clamp(self,v:float) -> float:
        v = max(self.min, min(self.max, v))
        if self.step > 0:
            v = round(v/self.step) * self.step
        return max(self.min, min(self.max, v))
    def set_on_change(self,cb):
        self.on_change = cb

    def _pos_to_value(self,px:int) -> float:
        ratio  = (px - self.track_rect.left) / self.track_rect.width
        return self._clamp(self.min + ratio * (self.max - self.min))
    def _val_to_pos(self) -> int:
        if self.max == self.min:
            return self.track_rect.left
        ratio = (self.value - self.min) / (self.max - self.min)
        return int(self.track_rect.left + ratio * self.track_rect.width)
    def draw(self,surface, font=None):
        pg.draw.rect(surface,(210,210,210),self.track_rect, border_radius=3)
        pg.draw.rect(surface,(60,60,60),self.track_rect,1, border_radius=3)

        hx= self._val_to_pos()
        hy= self.track_rect.centery
        pg.draw.circle(surface,(40,40,40), (hx, hy), self.handle_radius)
        if font and self.label:
            if callable(self.value_to_text):
                vtxt = self.value_to_text(self.value)
            else:
                vtxt = f"{int(self.value)}"
            text = font.render(f"{self.label}: {vtxt}", True, (0,0,0))
            surface.blit(text,(self.track_rect.left, self.track_rect.top - 28))
        self._hit_rect.center = (hx, hy)
    def handle_event(self,event):
        old = self.value
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.track_rect.collidepoint(event.pos) or self._hit_rect.collidepoint(event.pos):
                self.dragging = True
                self.valuue = self._pos_to_value(event.pos[0])
        elif event.type == pg.MOUSEMOTION and self.dragging:
            self.value = self._pos_to_value(event.pos[0])
        elif event.type == pg.MOUSEBUTTONUP and self.dragging:
            self.dragging = False
            self.value = self._pos_to_value(event.pos[0])
        if self.value != old and hasattr(self,'on_change') and self.on_change:
            self.on_change(self.value)

