from easy import easy
from faster import faster
from utils import greet, cyan, end

if __name__ == '__main__':
    greet()
    print('Which program do you want to run? For more information, read the README.md file.')
    print(f'Remember, {cyan}faster{end} might get you in trouble, but {cyan}easy{end} lets you grade yourself normally.')
    print('1) easy')
    print('2) faster')
    arg = input('Enter the number corresponding to your answer: ')
    if arg == 1:
        easy()
    else:
        faster()