import pyglet

class Tag(object):
    def __init__(self, text, font, color=(1,1,1,1)):
        self.text=pyglet.font.Text(font, text, color=color,
                halign="left", valign="bottom")

    @property
    def left(self):
        return self.text.x

    @property
    def right(self):
        return self.text.x+self.text.width

    @property
    def top(self):
        return self.text.y+self.text.height

    @property
    def bottom(self):
        return self.text.y

    def setPos(self,position):
        self.text.x=position[0]
        self.text.y=position[1]

    def collidesWith(self,tag):
        if self.left < tag.right and self.right > tag.left and \
                self.top > tag.bottom and self.bottom < tag.top:
               return True
        else:
            return False

    def draw(self):
        self.text.draw()
