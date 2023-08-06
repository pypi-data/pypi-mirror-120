import readline
from argparse import ArgumentParser

from .env import Env

CLEAR_SCREEN = '\033[2J'

prompt = 'zcalc> '

def cmd():
    parser = ArgumentParser()
    parser.add_argument('-r', '--raw', action='store_true')
    args = parser.parse_args()

    z = Env()

    if not args.raw:
        print(CLEAR_SCREEN)
    while True:
        try:
            line = input(prompt)
        except EOFError:
            return
        except KeyboardInterrupt:
            return
        z.do(line)
        if not args.raw:
            print(CLEAR_SCREEN)
        if z.output:
            print(z.output)
        else:
            for item in z.stack:
                print(item)
        print(f'(!) {z.error}' if z.error else '')

if __name__ == '__main__':
    cmd()
