import json
from pyautogui import press, keyDown, keyUp, write
from platform import system

cmd_alt = 'command' if system() == 'Darwin' else 'alt'

csi = '\x1B['
red = csi + '31;1m'
yellow = csi + '33;1m'
green = csi + '32;1m'
cyan = csi + '36;1m'
magenta = csi + '95;1m'
end = csi + '0m'

def get_data(default_comments):
    print('Because this is the first time I met you, I need some of your information.\n')
    d = {
        'name': input('What is your full name (First Last)? ').strip(),
        'sid': int(input('What is your SID? ').strip()),
        'email': input('What is your @berkeley.edu email?: ').strip()
    }
    while (d['email'][-13:] != '@berkeley.edu'):
        d['email'] = input('Please enter a valid @berkeley.edu email address: ')
    
    print()
    print('Which class are you taking? Enter the number corresponding to your answer:')
    print('1) EECS 16A')
    print('2) EECS 16B')

    d.update({
        'class': '16a' if input('Enter answer here: ').strip() == '1' else '16b',
        'comments': default_comments
    })

    with open('data.json', 'w') as data:
        data.write(json.dumps(d))
    
    return d

def alt_tab():
    keyDown(cmd_alt)
    press('tab')
    keyUp(cmd_alt)

def get_parts(prompt, parts):
    p = input(prompt).strip().split(' ')
    while not all(el in parts for el in p):
        print(f'{red}ERROR: Question not in this HW. Try again.{end}')
        p = input(prompt).strip().split(' ')
    return set(p)

def fill(num, d, scores, comments):
    s = str(num)
    for p in scores[num]:
        d['q' + p] = s
        if num < 10:
            d[f'q{p}-comment'] = next(comments)