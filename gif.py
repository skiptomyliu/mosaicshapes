
#!/usr/bin/python

import imageio
import argparse
import sys

def save_gif(filenames, filepath, duration):
    images = []
    for filename in filenames:
        images.append(imageio.imread(filename))
    kargs = { 'duration': duration }
    imageio.mimsave(filepath, images, 'GIF', **kargs)


def main():
    parser = argparse.ArgumentParser(description='Convert images to gif')
    parser.add_argument('images', metavar='N', type=str, nargs='+',
                        help='List of image filenames')
    parser.add_argument("-d", "--duration", default=0.1, type=float,  dest='duration',
                        help='delay between frames')

    args=parser.parse_args()

    print args.images
    print args.duration

    save_gif(args.images, "./happy.gif", args.duration)


if __name__ == "__main__":
    main()