
from PIL import Image
import os
import math
import util
import gc


def crop(im,height,width):

    imgwidth, imgheight = im.size
    rows = int(math.ceil(imgheight/float(height)))
    cols = int(math.ceil(imgwidth/float(width)))

    for i in range(rows):
        for j in range(cols):
            box = (
                j*width, 
                i*height, 
                util.clamp_int((j+1)*width, 0, imgwidth), 
                util.clamp_int((i+1)*height, 0, imgheight)
            )
            yield im.crop(box)


class Lego():
    class __init__():
        pass

    @staticmethod
    def divide_and_save(im, window, out_filename):
        files = []
        for k,piece in enumerate( crop(im,window,window) ):
            path=os.path.join('/tmp',"{f}-{i}.JPEG".format(f=out_filename, i=k))
            piece.save(path)
            files.append(path)

        return files

    @staticmethod
    def stitch(file_paths, cols, size):
        og = Image.new('RGB', size, 255)
        col,row = 0,0
        cur_w, cur_h = 0,0
        total_w = 0
        

        for f in file_paths:
            im = Image.open(f)
            w,h = im.size
            og.paste(im, (cur_w,cur_h))
            del im

            col = (col+1)%cols
            cur_w += w
            if col==0:
                row += 1
                cur_h += h
                total_w = cur_w
                cur_w = 0
            gc.collect()

        og = og.crop((0, 0, total_w, cur_h))
        return og
                    


