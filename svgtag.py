import pyglet

class Tag(object):
    def __init__(self, text, font, color=(1,1,1,1), padding=1):
        self.text = pyglet.font.Text(font, text,
                halign="left", valign="bottom")
        self.color = color
        self.padding = padding

    @property
    def left(self):
        return self.text.x

    @property
    def right(self):
        return self.text.x+self.text.width+self.padding

    @property
    def top(self):
        return self.text.y+self.text.height+self.padding

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

    def draw(self, canvas, padding=1):
        style = "font-family: {};\
                 font-size: {}pt;".format(self.text.font.name,
                                              self.text.font.size)

        color = "rgb({},{},{})".format(int(self.color[0]*255),
                                       int(self.color[1]*255),
                                       int(self.color[2]*255))
        pos = self.text.x, self.text.y

        canvas.add(
            canvas.text(self.text.text, insert=pos,
                        textLength=self.text.width+self.padding,
                        style=style,
                        fill = color)
            )
