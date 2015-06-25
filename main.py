#!/usr/local/bin/python
import pyglet
from pyglet.window import key
import itertools
from tag import Tag
from utils import hsv2rgb

# Create a window object
width,height = 1000, 600
window = pyglet.window.Window(width=width, height=height)
window.set_vsync(True)

# Use a decorater to register a custom action for the on_draw event
@window.event
def on_draw():
    window.clear()

    for tag in tags:
        tag.draw()

    pyglet.image.get_buffer_manager().get_color_buffer().save("screenshot.png")


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
    tag = Tag(word, f, hsv2rgb((i*inc+240)%360,0.9,0.8))

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
