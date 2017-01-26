

from grid import Grid
import argparse




def main():
    parser = argparse.ArgumentParser(description='Mosaic photos')

    parser.add_argument('photos', metavar='N', type=str, nargs='+',
                    help='Photo path')

    parser.add_argument("-d", "--diamond", action='store_true', 
        help="Use diamond grid instead of squares")
    parser.add_argument("-r", "--restrain", default=False, action='store_true', 
        help="Use diamond grid instead of squares")
    parser.add_argument("-e", "--enlarge", default=True, action='store_true', 
        help="Use diamond grid instead of squares")
    parser.add_argument("-m", "--multi", default=.014, type=float)

    args = parser.parse_args()

    if args.photos:
        photo_path = args.photos[0]
        grid = Grid(photo_path, pix_multi=args.multi, restrain=args.restrain, enlarge=args.enlarge)
        grid.n_pass(1)
        grid.save("./out.JPEG") 


if __name__ == "__main__":
    main()