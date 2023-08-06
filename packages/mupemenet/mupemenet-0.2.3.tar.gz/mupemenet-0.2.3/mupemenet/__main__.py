import sys
from mupemenet.App import main

if __name__ == "__main__":
    val = 'debug'
    if len(sys.argv) > 1:
        val = 'release' if sys.argv[1] == 'release' else 'debug'
    main(val)

