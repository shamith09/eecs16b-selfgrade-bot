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

    greet(ef)
    arg = input('Enter the number corresponding to your answer: ').strip()
    while not (arg == '1' or arg == '2'):
        print(f'{red}Please enter 1 or 2.{end}')
        arg = input('Enter the number corresponding to your answer: ').strip()

    print()
    program = ef["easy"] if arg == '1' else ef["faster"]
    print(f'Running {program}...\n')

    data_dict, parts = init(default_comments)

    if arg == '1':
        easy(data_dict, parts)
    else:
        faster(data_dict, parts)
    submit(data_dict['hwNum'])