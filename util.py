





def clamp_int(val, minval, maxval):
    if val < minval: return int(minval)
    if val > maxval: return int(maxval)

    return int(val)


def average_color(rect, image):
    x0,y0 = rect[0]
    x1,y1 = rect[1]
    r,g,b = 0,0,0

    w = abs(x0 - x1)
    h = abs(y0 - y1)

    area = w*h

    for x in range(x0, x1):
        for y in range(y0, y1):
            cr,cg,cb = image.getpixel((x,y))
            r+=cr
            g+=cg
            b+=cb

    return (r/area, g/area, b/area)

