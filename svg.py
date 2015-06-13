import svgwrite
from pyglet import font

f=font.load("Helvetica", 20)

def SizeText(render_font, text, padding=1):
    render = font.Text(render_font, text)
    return render.width+padding,render.height+padding

def AddText(drawing, text, render_font, pos, padding=1):
    render = font.Text(render_font, text)
    drawing.add(
            svg.text(text, insert=pos, textLength=render.width+padding,
                style="font-family: %s; font-size: %spt;"%(render_font.name, render_font.size))
           )
    return pos[0],pos[1],render.width+padding,render.height+padding

svg = svgwrite.Drawing("cloud.svg", size=(200,200), style="border: 1px solid black;")

msg = "Hi world"
sz=SizeText(f, msg)
AddText(svg, msg, f, ((200-sz[0])/2,200/2))

svg.save()
