





def clamp_int(val, minval, maxval):
    if val < minval: return int(minval)
    if val > maxval: return int(maxval)

    return int(val)


def average_color(rect, image):
    rect.x0
    rect.x1
    r,g,b = 0,0,0
    for x in range(rect.x0, rect.x1):
        for y in range(rect.y0, rect.y1):
            cr,cg,cb = image.getpixel((x,y))
            r+=cr
            g+=cg
            b+=cb

    return (r/(rect.area()), g/(rect.area()), b/(rect.area()))

