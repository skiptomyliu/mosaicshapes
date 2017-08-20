
from multiprocessing.dummy import Pool as ThreadPool
from grid import Grid
import argparse
import util
import math

def create_reg_images(photo_path, pix_multi, diamond, color, 
                      working_res, enlarge, pool, output_path):

    grid = Grid(photo_path, pix=0, pix_multi=pix_multi, diamond=diamond, colorful=color,
                working_res=working_res, enlarge=enlarge)

    total_updates = 20
    step_size = util.clamp_int(int(math.ceil(grid.rows/(1.0*total_updates))), 1, 10000)

    ending_index = step_size*total_updates
    # diff = grid.rows - step_size*total_updates

    todos = []
    for i in range(total_updates+1):
        s_index = step_size*i
        e_index = s_index + step_size
        todos.append((s_index, e_index, output_path))
        
        is_continue = False if e_index >= grid.rows else True
        if not is_continue:
            break

    # double check that we are not doing double work
    try:
        pool = ThreadPool(8)
        pool.map(grid.grid_start_end_thread, todos)
        pool.close()
        pool.join()
    except (KeyboardInterrupt, SystemExit):
        pool.terminate()

    grid.save(output_path)

    #
    #
    
    # print 100in
    # grid.grid_start_end(0, grid.rows)
    # grid.save(output_path)

    # if e_index < grid.rows:
    #     s_index = ending_index
    #     e_index = grid.rows
    #     grid.grid_start_end(s_index, e_index)
    #     grid.save(output_path)
    #     print 100

def main():
    parser = argparse.ArgumentParser(description='Mosaic photos')

    parser.add_argument('photos', metavar='N', type=str, nargs='+',
                        help='Photo path')
    parser.add_argument("-d", "--diamond", default=False, action='store_true',
                        help="Use diamond grid instead of squares")
    parser.add_argument("-c", "--color", default=False,
                        action='store', choices=["0", "1", "2"],
                        help="Specify color values")
    parser.add_argument("-a", "--analogous", default=False, action='store_true',
                        help="Use analogous color")
    parser.add_argument("-r", "--working_res", default=0, required=False, type=int,
                        help="Resolution to sample from")
    parser.add_argument("-e", "--enlarge", default=0, required=False, type=int,
                        help="Resolution to draw")
    parser.add_argument("-m", "--multi", default=.014, type=float)
    parser.add_argument("-p", "--pool", default=1, type=int)
    parser.add_argument("-o", "--out", default="/tmp/out.JPEG", type=str)

    args = parser.parse_args()

    if args.photos:
        photo_path = args.photos[0]
        # try:
        create_reg_images(photo_path, args.multi, args.diamond, args.color,
                          args.working_res, args.enlarge, args.pool, args.out)
        # except Exception as e:
            # print e
            # return 1
    return 0


if __name__ == "__main__":
    main()