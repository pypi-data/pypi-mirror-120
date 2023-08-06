import os
import sys
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_PATH)
print(BASE_PATH)

from App import main

if __name__ == "__main__":
    # execute only if run as a script
    main()

