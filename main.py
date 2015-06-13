#!/usr/local/bin/python
import pyglet
from pyglet.window import key
import itertools
import colorsys

# Load a font for rendering text ovals and the fps
helv_font=pyglet.font.load("Helvetica", 14)


class Tag(object):
    def __init__(self, text, color=(1,1,1,1), font=helv_font):
        self.text=pyglet.font.Text(font, text, color=color, halign="left", valign="bottom")

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
        #if ((tag.left <= self.right and tag.left >= self.left) or \
        #    (tag.right >= self.left and tag.right <= self.right)) and \
        #   ((tag.bottom <= self.top and tag.bottom >= self.bottom) or \
        #    (tag.top >= self.bottom and tag.top <= self.top)):
        #       return True
        if self.left < tag.right and self.right > tag.left and \
                self.top > tag.bottom and self.bottom < tag.top:
               return True
        else:
            return False

    def draw(self):
        self.text.draw()


# Create a window object
width,height = 1000, 600
window = pyglet.window.Window(width=width, height=height)
window.set_vsync(True)


# Use a decorater to register a custom action
# for the on_draw event
@window.event
def on_draw():
    window.clear()

    for tag in tags:
        tag.draw()

    pyglet.image.get_buffer_manager().get_color_buffer().save("screenshot.png")


def hsv2rgb(h,s,v,a=1):
    """
    h: 0-360
    s: 0-1
    v: 0-1
    """
    r,g,b=colorsys.hsv_to_rgb(h/360.0,s,v)
    return r,g,b,a

words = "Python C Rust C++ C# Java Objective-C Erlang Elixir Haskell PHP Swift SQL bash fish Assembly lisp XML json YAML markdown Ruby Perl R HTML CSS".split(" ")

colors = [ (0.7,  0,  0,1), # Red
           (0.7,  0,0.9,1), # Pink/purple
           (0.8,0.4,  0,1), # Orange
           (0.8,0.8,0.8,1), # White
           (0.2,0.3,0.9,1), # Blue
           (  0,0.7,  0,1), # Green
           (  0,0.8,0.8,1)  # Cyan
         ]
colors = [ (0.6, 0.6, 0.6, 1) ]
colors_cycle = itertools.cycle(colors)


padding = 3
tags = []
size = float(len(words))
inc=360/size

for i,word in enumerate(words):
    added = False
    f=pyglet.font.load("Helvetica", (size-i/1.125)*3.25) #(size-i/1.5)-0.3*size)#int(len(word)*3))
    #tag = Tag(word, colors.next(), font = f)
    tag = Tag(word, hsv2rgb((i*inc+240)%360,0.9,0.8), font = f)

    positions = [(width/2-tag.text.width/2,height/2-tag.text.height/2)]
    for t in tags:
        positions.append((t.left          , t.top+padding))
        positions.append((t.right+padding , t.bottom))
        positions.append((t.left          , t.bottom-tag.text.height-padding))
        positions.append((t.left-tag.text.width-padding, t.bottom))

    while not added:
        try_pos = positions.pop(0)
        tag.setPos(try_pos)
        added=True
        if tag.left < 0 or tag.bottom < 0 or \
           tag.top > height or tag.right > width:
            added=False
            continue

        for t in tags:
            if tag.collidesWith(t):
                added=False
                break

    tags.append(tag)

##pyglet.clock.schedule_interval(main_update, 1/60.0)
##window.push_handlers(pyglet.window.event.WindowEventLogger())

pyglet.app.run()
