
import colorsys

def clamp_int(val, minval, maxval):
    if val < minval: return int(minval)
    if val > maxval: return int(maxval)

    return int(val)


def average_color_pixels(image, pixels):
    r,g,b = 0,0,0
    for pixel in pixels:
        x,y = pixel
        cr,cg,cb = image.getpixel((x,y))
        r+=cr
        g+=cg
        b+=cb

    total = len(pixels)
    return (r/total, g/total, b/total)



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


DEG30 = 40/360.

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




rgb_scale = 255
cmyk_scale = 100
def rgb_to_cmyk(r,g,b):
    if (r == 0) and (g == 0) and (b == 0):
        # black
        return 0, 0, 0, cmyk_scale

    # rgb [0,255] -> cmy [0,1]
    c = 1 - r / float(rgb_scale)
    m = 1 - g / float(rgb_scale)
    y = 1 - b / float(rgb_scale)

    # extract out k [0,1]
    min_cmy = min(c, m, y)
    c = (c - min_cmy) 
    m = (m - min_cmy) 
    y = (y - min_cmy) 
    k = min_cmy

    # rescale to the range [0,cmyk_scale]
    return c*cmyk_scale, m*cmyk_scale, y*cmyk_scale, k*cmyk_scale

    # return clamp_int(c*cmyk_scale, 25, 100), clamp_int(m*cmyk_scale, 25, 100),  clamp_int(y*cmyk_scale, 25, 100),  clamp_int(k*cmyk_scale, 25, 100)

def cmyk_to_rgb(c,m,y,k):
    """
    """
    r = rgb_scale*(1.0-(c+k)/float(cmyk_scale))
    g = rgb_scale*(1.0-(m+k)/float(cmyk_scale))
    b = rgb_scale*(1.0-(y+k)/float(cmyk_scale))
    return int(r),int(g),int(b)





