import sys
from ipysketch.app import main

if __name__ == '__main__':
    try:
        name = sys.argv[1]
    except:
        print('Invalid or missing sketch name')
    main(name)

