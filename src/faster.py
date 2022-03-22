from fileinput import close
from time import sleep
from splinter import Browser
from random import shuffle
from pyautogui import keyDown, write
import json

from utils import *

# Default comments
default_comments = ['Calculation error', 'Misread question']

print('\nHello! My name is 16Bot, made by a lazy CS & Physics major named Shamith Pasula.')
print('I will be doing your 16A or 16B self-grade for you, giving you 8/10 on random questions to not be sus.')
print('The comments for the 8/10 questions are in data.json, edit them if you wish.')
print('If this isn\'t your first time meeting me and you want to update your data, delete data.json and run faster.py again.')
print('If you mess up or want to restart, press Ctrl+C and run faster.py again. \n')

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
    print('\nI have your name, email, and SID already!\n')
except:
    while True:
        try:
            print('I have a few questions for you:\n')
            get_data(data_dict, default_comments)
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
    indices = list(range(len(inputs)))
    shuffle(indices)

    print(f'There are {len(indices)} questions on this HW.')
    print()

    num_incorrects = int(input('How many questions out of these do you want to give an 8/10? ').strip())
    print('I will now do your self-grade for you! I\'ll mark random questions as 8/10 and the rest as 10/10.')

    print(yellow + 'IMPORTANT: Do not touch the keyboard or mouse until I am done.' + end)

    print()
    for i in range(5):
        print(f'{cyan}Beginning self-grade in {5 - i} seconds.{end}', end='\r')
        sleep(1)
    print('\nSelf-grading now...')

    alt_tab()

    q, r = divmod(num_incorrects, len(data_dict['comments']))
    comments = iter(q * data_dict['comments'] + data_dict['comments'][:r])

    for i in indices[:-num_incorrects]:
        browser.find_by_value('10')[i].click()

    for i in indices[-num_incorrects:]:
        browser.find_by_value('8')[i].click()
        keyDown('tab')
        write(next(comments))

        
    browser.find_by_id('d' + difficulty).click()
    browser.find_by_id('Hours Spent').fill(hours_spent)
    browser.find_by_id('Teammate Headcount').fill(num_teammates)
    browser.find_by_id(went_to_hw_party).click()
    browser.find_by_xpath('/html/body/section/form/p/button').click()
    browser.find_by_id('json-download').click()

    sleep(3)

print()
print('Submit the downloaded .json file to Gradescope and you\'re done! Have a great day!\n')