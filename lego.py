
from PIL import Image
import os

def crop(im,height,width):
    imgwidth, imgheight = im.size
    for i in range(imgheight//height):
        for j in range(imgwidth//width):
            box = (j*width, i*height, (j+1)*width, (i+1)*height)
            yield im.crop(box)

class Lego():
    class __init__():
        pass

    @staticmethod
    def divide_and_save(im, out_filename):
        height=500
        width=500
        start_num=0
        files = []
        for k,piece in enumerate( crop(im,height,width),start_num ):
                img=Image.new('RGB', (height,width), 255)
                img.paste(piece)
                path=os.path.join('/tmp',"{f}-{i}.JPEG".format(f=out_filename, i=k))
                img.save(path)
                files.append(path)

        return files

    @staticmethod
    def stitch(file_paths, rows, cols, size):
        og = Image.new('RGB', (height,width), 255)
        for f in file_paths:
            im = Image.open(f)


