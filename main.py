from resources.lib.entry import run
import sys
import xbmc


if __name__ == '__main__':
    # debug log
    xbmc.log(f'== [Clex] == {sys.argv}', level=1)
    run()
