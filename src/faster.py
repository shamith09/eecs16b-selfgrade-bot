from random import shuffle
from json import dumps

from utils import *

# Default comments
def faster(data_dict, parts):
    shuffle(parts)

    print(f'There are {len(parts)} questions on this HW.')
    print()

    num_incorrects = int(input('How many questions out of these do you want to give an 8/10? ').strip())

    out_dict, comments = get_out(data_dict)

    for p in parts[:-num_incorrects]:
        out_dict['q' + p] = "10"

    for p in parts[-num_incorrects:]:
        out_dict['q' + p] = "8"
        out_dict[f'q{p}-comment'] = next(comments)
        
    with open(f'out/selfgrades-{data_dict["hwNum"]}.json', 'w') as out:
        out.write(dumps(out_dict))

    print()
    print(f'Submit the selfgrades-{data_dict["hwNum"]}.json file in the out folder to Gradescope and you\'re done! Have a great day!\n')