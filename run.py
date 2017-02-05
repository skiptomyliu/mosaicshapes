

from grid import Grid
import argparse
import util
import math


def create_reg_images(photo_path, pix_multi, diamond, colorful, restrain, enlarge, output_path):
    grid = Grid(photo_path, pix=0, pix_multi=pix_multi, diamond=diamond, colorful=colorful, 
        restrain=restrain, enlarge=enlarge)
    # XXX: enforce minimum image size
    total_updates = 20
    step_size = util.clamp_int(int(math.ceil(grid.rows/(1.0*total_updates))), 1, 10000)

    ending_index = step_size*total_updates
    diff = grid.rows - step_size*total_updates

    


    for i in range(total_updates+1):
        s_index = step_size*i
        e_index = s_index + step_size
        grid.grid_start_end(s_index, e_index)
        progress_percent = int(round(((i*step_size)/float(grid.rows))*100))

        is_continue = False if e_index >= grid.rows else True
        grid.save(output_path, is_continue=is_continue)
        print progress_percent
        if not is_continue:
            break

    if e_index < grid.rows:
        s_index = ending_index
        e_index = grid.rows
        grid.grid_start_end(s_index, e_index)
        grid.save(output_path)
        print 100

def main():
    parser = argparse.ArgumentParser(description='Mosaic photos')

    parser.add_argument('photos', metavar='N', type=str, nargs='+',
                    help='Photo path')
    parser.add_argument("-d", "--diamond", default=False, action='store_true', 
        help="Use diamond grid instead of squares")
    parser.add_argument("-c", "--colorful", default=False, action='store_true', 
        help="Use diamond grid instead of squares")
    parser.add_argument("-r", "--restrain", default=False, action='store_true', 
        help="Use diamond grid instead of squares")
    parser.add_argument("-e", "--enlarge", default=0, required=False, type=int, 
        help="Use diamond grid instead of squares")
    parser.add_argument("-m", "--multi", default=.014, type=float)
    parser.add_argument("-o", "--out", default="/tmp/out.JPEG", type=str);

    args = parser.parse_args()

    if args.photos:
        photo_path = args.photos[0]
        # grid = Grid(photo_path, pix_multi=args.multi, restrain=args.restrain, enlarge=args.enlarge)
        # grid.n_pass(1)
        # grid.save("/tmp/out.JPEG")
        create_reg_images(photo_path, args.multi, args.diamond, args.colorful, 
            args.restrain, args.enlarge, args.out)



if __name__ == "__main__":
    main()