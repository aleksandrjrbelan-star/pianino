from settings import WHITE, BLACK, GREY
from pygame import Rect, mouse, draw, MOUSEBUTTONDOWN

class Button:
    def __init__(self,x,y,w,h,text,action=None):
        self.rect = Rect(x,y,w,h)
        self.text = text
        self.action = action
        self.idle = GREY
        self.hover = (180,180,180)
        self.border = BLACK
        self.text_color = BLACK
    def draw(self,screen,font):
        mouse_pos = mouse.get_pos( )
        color = self.hover if self.rect.collidepoint(mouse_pos) else self.idle

        draw.rect(screen,color,self.rect)
        draw.rect(screen,self.border,self.rect,2)

        text_surf = font.render(self.text,1,self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf,text_rect)
    def handle_event(self,event):
        if event.type == MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos) and self.action:
                    self.action()