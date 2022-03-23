import json

from utils import *

# Default comments
def easy():
    default_comments = ['Calculation error', 'Misread question']

    data_dict = ask_user(default_comments)
    more_qs(data_dict)
    parts = get_inputs(data_dict)

    print(f'There are {len(parts)} questions on this HW.')
    print('These are the parts:')
    p_str = parts[0]
    for i in range(1, len(parts)):
        p_str += ', ' + parts[i]
    print(p_str)

    print(f'\nWhat questions do you want to grade as a {red}0{end}, {magenta}2{end}, {yellow}5{end}, {cyan}8{end}, or {green}10{end}?')
    print('Enter the question parts with spaces in between (e.g. 1a 10c 9d) next to the score you want to give them.')
    print('I will only ask for the questions you want to give less than a 10, and fill in the rest as 10\'s.\n')
    print('If no questions correspond a specific score, just press enter to move onto the next.')

    scores = {
        0: get_parts(f'{red}0{end}: ', parts),
        2: get_parts(f'{magenta}2{end}: ', parts),
        5: get_parts(f'{yellow}5{end}: ', parts),
        8: get_parts(f'{cyan}8{end}: ', parts)
    }
    scores[10] = set(parts).symmetric_difference(scores[0].union(scores[2].union(scores[5].union(scores[8]))))

    comments = infinite_gen(data_dict['comments'])
    out_dict = data_dict.copy()
    out_dict.pop('class')
    out_dict.pop('comments')

    for n in scores:
        easy_fill(n, out_dict, scores, comments)

    with open(f'out/selfgrades-{data_dict["hwNum"]}.json', 'w') as out:
        out.write(json.dumps(out_dict))

    print()
    print(f'Submit the selfgrades-{data_dict["hwNum"]}.json file in the out folder to Gradescope and you\'re done! Have a great day!\n')