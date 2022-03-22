from fileinput import close
from time import sleep
from splinter import Browser
import json
import re

from utils import *

# Default comments
default_comments = ['Calculation error', 'Misread question']

print('\nHello! My name is 16Bot, made by a lazy CS & Physics major named Shamith Pasula.')
print('I will be doing your 16A or 16B self-grade for you, giving you whichever grade you want for each question.')
print('The comments for the 8/10 questions are in data.json, edit them if you wish.')
print('If this isn\'t your first time meeting me and you want to update your data, delete data.json and run easy.py again.')
print('If you mess up or want to restart, press Ctrl+C and run easy.py again. \n')

# params
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
            data_dict = get_data(default_comments)
            break
        except ValueError:
            print(red + '\nERROR: Bad input. Restarting.\n' + end)

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
            print('Please enter Y or N.')
            data_dict['Attended HW Party'] = input('Did you go to HW party (Enter Y or N)? ').strip().upper()
        break
    except ValueError:
        print(red + '\nERROR: Bad input. Restarting.\n' + end)

print()
for i in range(5):
    print(f'{cyan}A new Google Chrome window will open in a new window in {5 - i} seconds. I will navigate back to the terminal to ask you one last question.{end}', end = '\r')
    sleep(1)
print('\nOpening now...')
close()

with Browser('chrome') as browser:
    try:
        url = f'http://www.eecs{data_dict["class"]}.org/self-grade-{data_dict["hwNum"]}.html'
    except:
        print(f'{red}ERROR: Self-grade for this HW has either not released yet or this HW doesn\'t exist. Restarting.{end}')
    browser.visit(url)

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
        0: get_parts(f'{red}0{end}: ', parts),
        2: get_parts(f'{magenta}2{end}: ', parts),
        5: get_parts(f'{yellow}5{end}: ', parts),
        8: get_parts(f'{cyan}8{end}: ', parts)
    }
    num_incorrects = sum(len(scores[k]) for k in scores)
    scores[10] = set(parts).symmetric_difference(scores[0].union(scores[2].union(scores[5].union(scores[8]))))

    print('\nI will now do your self-grade for you! I\'ll fill in the comments with the list in data.json.')

    q, r = divmod(num_incorrects, len(data_dict['comments']))
    comments = iter(q * data_dict['comments'] + data_dict['comments'][:r])

    with open(f'out/selfgrades-{data_dict["hwNum"]}.json', 'w') as out:
        data_dict.pop('class')
        data_dict.pop('comments')
        for n in scores:
            fill(n, data_dict, scores, comments)
        out.write(json.dumps(data_dict))

print()
print('Submit the downloaded .json file to Gradescope and you\'re done! Have a great day!\n')