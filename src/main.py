from easy import easy
from faster import faster

from utils import *

# EDIT THESE IF YOU WANT TO CHANGE THE DEFAULT COMMENTS
# OR GO INTO data.json TO CHANGE THEM
default_comments = ['Calculation error', 'Misread question']

if __name__ == '__main__':
    ef = {
        'easy': f'{cyan}easy{end}',
        'faster': f'{red}faster{end}'
    }

    greet()
    print('Which program do you want to run? For more information, read the README.md file.')
    print(f'Remember, {ef["easy"]} lets you grade yourself normally, but {ef["faster"]} might get you in trouble.')
    print(f'1) {ef["easy"]}')
    print(f'2) {ef["faster"]}')

    arg = input('Enter the number corresponding to your answer: ')
    print()
    program = ef["easy"] if arg == '1' else ef["faster"]
    print(f'Running {program}...\n')

    data_dict, parts = init(default_comments)

    if arg == '1':
        easy(data_dict, parts)
    else:
        faster(data_dict, parts)