from sys import argv
from easy import easy
from faster import faster

if __name__ == '__main__':
    if len(argv) == 0 or argv[1] == easy:
        easy()
    else:
        faster()