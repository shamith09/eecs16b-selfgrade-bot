import json, re
from pyautogui import press, keyDown, keyUp
from platform import system
from time import sleep
from splinter import Browser
from fileinput import close

cmd_alt = 'command' if system() == 'Darwin' else 'alt'
wait_time = 3

csi = '\x1B['
red = csi + '31;1m'
yellow = csi + '33;1m'
green = csi + '32;1m'
cyan = csi + '36;1m'
magenta = csi + '95;1m'
end = csi + '0m'

def greet():
    print('\nHello! My name is 16Bot, made by a lazy CS & Physics major named Shamith Pasula.')
    print('I will be doing your 16A or 16B self-grade for you, giving you 8/10 on random questions to not be sus.')
    print('The comments for the incorrect questions are in data.json, edit them if you wish.')
    print('If this isn\'t your first time meeting me and you want to update your data, delete data.json and run the program again.')
    print('If you mess up or want to restart, press Ctrl+C and run the program again. \n')

def ask_user(default_comments):
    try:
        data_dict = open('bin/data.json', 'r')
        data_dict = json.load(data_dict)
        if 'comments' not in data_dict:
            data_dict['comments'] = default_comments
            with open('data.json', 'w') as data:
                data.write(json.dumps(data_dict))
        if 'class' not in data_dict:
            print('Which class are you taking? Enter the number corresponding to your answer:')
            print('1) EECS 16A')
            print('2) EECS 16B')
            data_dict['class'] = '16A' if input('Enter answer here: ').strip() == '1' else '16B'
            with open('data.json', 'w') as data:
                data.write(json.dumps(data_dict))
            print()
        print('I have your name, email, and SID already!\n')
    except:
        while True:
            try:
                print('I have a few questions for you:\n')
                return get_data(default_comments)
            except ValueError:
                print(red + '\nERROR: Bad input. Restarting.\n' + end)
    return data_dict

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

def more_qs(data_dict):
    while True:
        try:
            data_dict['hwNum'] = int(input('Which homework are you self-grading? ').strip())
            if data_dict['hwNum'] < 10:
                data_dict['hwNum'] = '0' + str(data_dict['hwNum'])
            else:
                data_dict['hwNum'] = str(data_dict['hwNum'])

            if data_dict['class'] == '16b':
                data_dict['resubmission'] = 'no'
                while (data_dict['resubmission'] != 'Y' and data_dict['resubmission'] != 'N'):
                    data_dict['resubmission'] = input('Is this a resubmission (Enter Y or N)? ').strip().upper()
                data_dict['resubmission'] = 'yes' if data_dict['resubmission'] == 'Y' else 'no'

            data_dict.update({
                'Problem Set Difficulty': str(int(input(f'How difficult was HW {data_dict["hwNum"]} (Enter an integer between 1-10)? ').strip())),
                'Hours Spent': str(int(input(f'How many hours did you spend on HW {data_dict["hwNum"]}? ').strip())),
                'Teammate Headcount': str(int(input('How many people did you work with? ').strip())),
                'Attended HW Party': input('Did you go to HW party (Enter Y or N)? ').strip().upper()
            })

            while (data_dict['Attended HW Party'] != 'Y' and data_dict['Attended HW Party'] != 'N'):
                print(f'{red}Please enter Y or N.{end}')
                data_dict['Attended HW Party'] = input('Did you go to HW party (Enter Y or N)? ').strip().upper()
            break
        except ValueError:
            print(red + '\nERROR: Bad input. Restarting.\n' + end)
        close()

def alt_tab():
    keyDown(cmd_alt)
    press('tab')
    keyUp(cmd_alt)

def get_inputs(data_dict):
    print()
    for i in range(wait_time):
        print(f'{cyan}A new Google Chrome window will open in a new window in {wait_time - i} seconds, then I will navigate back to the terminal.{end}', end = '\r')
        sleep(1)
    print('\nOpening now...')

    with Browser('chrome') as browser:
        try:
            url = f'http://www.eecs{data_dict["class"]}.org/self-grade-{data_dict["hwNum"]}.html'
        except:
            print(f'{red}ERROR: Self-grade for this HW has either not released yet or this HW doesn\'t exist. Restarting.{end}')
        browser.visit(url)
        alt_tab()
        inputs = browser.find_by_value('Comment')

        parts = [re.search(r'q(.+)-comment', el['for']).group(1) for el in inputs]
    
    return parts

def get_parts(prompt, parts):
    p = input(prompt).strip().split(' ')
    while not all(el in parts or not el for el in p):
        print(f'{red}ERROR: Question not in this HW. Try again.{end}')
        p = input(prompt).strip().lower().split(' ')
    return set(p)

def infinite_gen(arr):
    yield from arr
    yield from infinite_gen(arr)

def easy_fill(num, d, scores, comments):
    s = str(num)
    for p in scores[num]:
        d['q' + p] = s
        if 0 < num < 10:
            d[f'q{p}-comment'] = next(comments)