from json import dumps

from utils import *

# Default comments
def easy(data_dict, parts):
    print(f'There are {len(parts)} questions on this HW.')
    print('These are the parts:')
    p_str = parts[0]
    for i in range(1, len(parts)):
        p_str += ', ' + parts[i]
    print(p_str)

    print(f'\nWhat questions do you want to grade as a {red}0{end}, {magenta}2{end}, {yellow}5{end}, {cyan}8{end}, or {green}10{end}?')
    print(f'Enter the question parts with {yellow}spaces in between (e.g. 1a 10c 9d){end} next to the score you want to give them.')
    print('I will only ask for the questions you want to give less than a 10, and fill in the rest as 10\'s.\n')
    print('If no questions correspond a specific score, just press enter to move onto the next.')

    scores = {
        0: get_parts(f'{red}0{end}: ', parts),
        2: get_parts(f'{magenta}2{end}: ', parts),
        5: get_parts(f'{yellow}5{end}: ', parts),
        8: get_parts(f'{cyan}8{end}: ', parts)
    }
    scores[10] = set(parts).symmetric_difference(scores[0].union(scores[2].union(scores[5].union(scores[8]))))

    out_dict, comments = get_out(data_dict)
    for n in scores:
        easy_fill(n, out_dict, scores, comments)

    write(data_dict['hwNum'], out_dict)
