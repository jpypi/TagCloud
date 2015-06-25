import colorsys

def hsv2rgb(h,s,v,a=1):
    """
    h: 0-360
    s: 0-1
    v: 0-1
    """
    r,g,b=colorsys.hsv_to_rgb(h/360.0,s,v)
    return r,g,b,a
