import argparse

from battlematica import GameEngine, GameDisplayProcess


if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument('-t', type=int, help='n. of ticks to execute')
    parser.add_argument('-f', type=str, help='game setting file')
    parser.add_argument('-d', help='display game graphically', action='store_true')
    parser.add_argument('-s', type=float, help='display speed x', default=1.0)
    parser.add_argument('-a', type=str, help='display assets archive', default=None)

    args = parser.parse_args()

    ge = GameEngine()
    ge.init_from_files(args.f)

    # setup display
    if args.d:
        if args.a is not None:
            gd = GameDisplayProcess(ge, speed=args.s, asset_archive=args.a)
        else:
            gd = GameDisplayProcess(ge, speed=args.s)
            gd.start()

    # calculate game
    ge.run_game(args.t)

    # join display process
    if args.d:
        gd.join()

