from random import shuffle
import json

from utils import *

# Default comments
default_comments = ['Calculation error', 'Misread question']

greet()
data_dict = ask_user(default_comments)
more_qs(data_dict)
parts = get_inputs(data_dict)

shuffle(parts)

print(f'There are {len(parts)} questions on this HW.')
print()

num_incorrects = int(input('How many questions out of these do you want to give an 8/10? ').strip())

comments = infinite_gen(data_dict['comments'])
out_dict = data_dict.copy()
out_dict.pop('class')
out_dict.pop('comments')

for p in parts[:-num_incorrects]:
    out_dict['q' + p] = "10"

for p in parts[-num_incorrects:]:
    out_dict['q' + p] = "8"
    out_dict[f'q{p}-comment'] = next(comments)
    
with open(f'out/selfgrades-{data_dict["hwNum"]}.json', 'w') as out:
    out.write(json.dumps(out_dict))

print()
print(f'Submit the selfgrades-{data_dict["hwNum"]}.json file in the out folder to Gradescope and you\'re done! Have a great day!\n')