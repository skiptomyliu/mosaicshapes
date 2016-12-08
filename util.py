
import colorsys

def clamp_int(val, minval, maxval):
    if val < minval: return int(minval)
    if val > maxval: return int(maxval)

    return int(val)


def average_color(image, rect=None):
    if not rect:            # Use whole image
        w,h = image.size
        x0,y0 = (0,0)
        x1,y1 = (w,h)
        print image.size
    else:                   # Use subset rect of image
        x0,y0,x1,y1 = rect
        w = abs(x0 - x1)
        h = abs(y0 - y1)

    r,g,b = 0,0,0
    area = w*h

    for x in range(x0, x1):
        for y in range(y0, y1):
            cr,cg,cb = image.getpixel((x,y))
            r+=cr
            g+=cg
            b+=cb

    return (r/area, g/area, b/area)


DEG30 = 30/360.

def adjacent_colors((r, g, b), d=DEG30): # Assumption: r, g, b in [0, 255]
    r, g, b = map(lambda x: x/255., [r, g, b]) # Convert to [0, 1]
    h, l, s = colorsys.rgb_to_hls(r, g, b)     # RGB -> HLS
    h = [(h+d) % 1 for d in (-d, d)]           # Rotation by d

    adjacent = [map(lambda x: int(round(x*255)), colorsys.hls_to_rgb(hi, l, s))
            for hi in h] # H'LS -> new RGB

    adjacent[0] = tuple(adjacent[0])
    adjacent[1] = tuple(adjacent[1])

    # import pdb; pdb.set_trace()
    return adjacent







