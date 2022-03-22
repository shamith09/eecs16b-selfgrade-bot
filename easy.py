from fileinput import close
from time import sleep
from splinter import Browser
from platform import system
from pyautogui import press, keyDown, keyUp, write
import json
import re

# Default comments
default_comments = ['Calculation error', 'Misread question']

csi = '\x1B['
red = csi + '31;1m'
yellow = csi + '33;1m'
green = csi + '32;1m'
cyan = csi + '36;1m'
magenta = csi + '95;1m'
end = csi + '0m'

cmd_alt = 'command' if system() == 'Darwin' else 'alt'

print('\nHello! My name is 16Bot, made by a lazy CS & Physics major named Shamith Pasula.')
print('I will be doing your 16A or 16B self-grade for you, giving you whichever grade you want for each question.')
print('The comments for the 8/10 questions are in data.json, edit them if you wish.')
print('If this isn\'t your first time meeting me and you want to update your data, delete data.json and run easy.py again.')
print('If you mess up or want to restart, press Ctrl+C and run easy.py again. \n')

def get_data():
    print('Because this is the first time I met you, I need some of your information.\n')
    data_dict['name'] = input('What is your full name (First Last)? ').strip()
    data_dict['sid'] = int(input('What is your SID? ').strip())
    data_dict['email'] = input('What is your @berkeley.edu email?: ').strip()
    while (data_dict['email'][-13:] != '@berkeley.edu'):
        data_dict['email'] = input('Please enter a valid @berkeley.edu email address: ')
    print()
    print('Which class are you taking? Enter the number corresponding to your answer:')
    print('1) EECS 16A')
    print('2) EECS 16B')
    data_dict['class'] = '16a' if input('Enter answer here: ').strip() == '1' else '16b'
    data_dict['comments'] = default_comments

    with open('data.json', 'w') as data:
        data.write(json.dumps(data_dict))

def get_parts(prompt):
        p = input(prompt).strip().split(' ')
        while not all(el in parts for el in p):
            print(f'{red}ERROR: Question not in this HW. Try again.{end}')
            p = input(prompt).strip().split(' ')
        return set(p)

def fill(num):
    s = str(num)
    for part in scores[num]:
        i = parts.index(part)
        browser.find_by_value(s)[i].click()
        if num != 10:
            keyDown('tab')
            write(next(comments))

def alt_tab():
    keyDown(cmd_alt)
    press('tab')
    keyUp(cmd_alt)

# params
try:
    data_dict = open('data.json', 'r')
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
            get_data()
            break
        except ValueError:
            print(red + '\nERROR: Bad input. Restarting.\n' + end)

while True:
    try:
        hw_number = int(input('Which homework are you self-grading? ').strip())
        if hw_number < 10:
            hw_number = '0' + str(hw_number)
        else:
            hw_number = str(hw_number)

        if data_dict['class'] == '16b':
            resubmission = 'no'
            while (resubmission != 'Y' and resubmission != 'N'):
                resubmission = input('Is this a resubmission (Enter Y or N)? ').strip().upper()
            resubmission = 'yes' if resubmission == 'Y' else 'no'

        difficulty = int(input(f'How difficult was HW {hw_number} (Enter an integer between 1-10)? ').strip())
        hours_spent = int(input(f'How many hours did you spend on HW {hw_number}? ').strip())
        print()
        num_teammates = int(input('How many people did you work with? ').strip())

        went_to_hw_party = None
        while (went_to_hw_party != 'Y' and went_to_hw_party != 'N'):
            went_to_hw_party = input('Did you go to HW party (Enter Y or N)? ').strip().upper()
        break
    except ValueError:
        print(red + '\nERROR: Bad input. Restarting.\n' + end)

print()
for i in range(5):
    print(f'{cyan}A new Google Chrome window will open in a new window in {5 - i} seconds. I will navigate back to the terminal to ask you one last question.{end}', end = '\r')
    sleep(1)
print('\nOpening now...')

with Browser('chrome') as browser:
    difficulty = str(difficulty)
    try:
        url = f'http://www.eecs{data_dict["class"]}.org/self-grade-{hw_number}.html'
    except:
        print(f'{red}ERROR: Self-grade for this HW has either not released yet or this HW doesn\'t exist. Restarting.')
    browser.visit(url)

    for s in ['name', 'email', 'sid']:
        browser.find_by_id(s).fill(data_dict[s])
    close()

    if data_dict['class'] == '16b':
        browser.find_by_value(resubmission).click()
    alt_tab()

    inputs = browser.find_by_value('Comment')
    parts = [re.search(r'q(.+)-comment', el['for']).group(1) for el in inputs]

    print(f'There are {len(inputs)} questions on this HW.')
    print('These are the parts:')
    p_str = parts[0]
    for i in range(1, len(parts)):
        p_str += ', ' + parts[i]
    print(p_str)

    print(f'\nWhat questions do you want to grade as a {red}0{end}, {magenta}2{end}, {yellow}5{end}, {cyan}8{end}, or {green}10{end}?')
    print('Enter the question parts with spaces in between (e.g. 1a 10c 9d) next to the score you want to give them.')
    print('I will only ask for the questions you want to give less than a 10, and fill in the rest as 10\'s.\n')

    scores = {
        0: get_parts(f'{red}0{end}: '),
        2: get_parts(f'{magenta}2{end}: '),
        5: get_parts(f'{yellow}5{end}: '),
        8: get_parts(f'{cyan}8{end}: ')
    }
    num_incorrects = sum(len(scores[k]) for k in scores)
    scores[10] = set(parts).symmetric_difference(scores[0].union(scores[2].union(scores[5].union(scores[8]))))

    print('\nI will now do your self-grade for you! I\'ll fill in the comments with the list in data.json.')
    print(yellow + 'IMPORTANT: Do not touch the keyboard or mouse until I am done.' + end)

    print()
    for i in range(5):
        print(f'{cyan}Beginning self-grade in {5 - i} seconds.{end}', end='\r')
        sleep(1)
    print('\nSelf-grading now...')
    alt_tab()

    q, r = divmod(num_incorrects, len(data_dict['comments']))
    comments = iter(q * data_dict['comments'] + data_dict['comments'][:r])

    for key in scores:
        fill(key)
        
    browser.find_by_id('d' + difficulty).click()
    browser.find_by_id('Hours Spent').fill(hours_spent)
    browser.find_by_id('Teammate Headcount').fill(num_teammates)
    browser.find_by_id(went_to_hw_party).click()
    browser.find_by_xpath('/html/body/section/form/p/button').click()
    browser.find_by_id('json-download').click()

    sleep(3)

print()
print('Submit the downloaded .json file to Gradescope and you\'re done! Have a great day!\n')