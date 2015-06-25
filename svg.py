import itertools
import svgwrite
from pyglet import font
from svgtag import Tag
from utils import hsv2rgb


def SizeText(render_font, text, padding=1):
    render = font.Text(render_font, text)
    return render.width+padding,render.height+padding


def AddText(drawing, text, render_font, pos, padding=1):
    render = font.Text(render_font, text)
    drawing.add(
            drawing.text(text, insert=pos, textLength=render.width+padding,
                style="font-family: %s; font-size: %spt;"%(render_font.name, render_font.size))
           )
    return pos[0],pos[1],render.width+padding,render.height+padding


def CheckCollision(tag1, tag2):
    if tag1[0] < tag2[0]+tag2[2] and tag1[0]+tag1[2] > tag2[0] and\
            tag1[1] > tag2[1]+tag2[3] and tag1[1]+tag2[3] < tag2[1]:
                return True
    else:
        return False


if __name__ == "__main__":
    words = "Python C Rust C++ C# Java Objective-C Erlang Elixir Haskell PHP"# Swift SQL bash fish Assembly lisp XML json YAML markdown Ruby Perl R HTML CSS"
    words = words.split(" ")

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

    width, height = 900, 500
    svg_drawing = svgwrite.Drawing("cloud.svg", size=(width, height),
                             style="border: 1px solid black;")
    fnt = font.load("Helvetica", 12 )
    sz = SizeText(fnt, "hello",0)
    AddText(svg_drawing,"hello",fnt,(0,sz[1]),0)


    padding = 3
    tags = []
    size = float(len(words))
    inc=360/size

    for i,word in enumerate(words):
        added = False
        f=font.load("Helvetica", (size-i/1.125)*2.25) #(size-i/1.5)-0.3*size)#int(len(word)*3))
        tag = Tag(word, f, hsv2rgb((i*inc+240)%360,0.9,0.8),0)

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
        tag.draw(svg_drawing)


    svg_drawing.save()
