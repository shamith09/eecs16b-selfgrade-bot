from fileinput import close
from time import sleep
from splinter import Browser
from random import shuffle
from platform import system
import pyautogui
import json

# Default comments
default_comments = ['Calculation error', 'Misread question']

csi = '\x1B['
red = csi + '31;1m'
yellow = csi + '33;1m'
cyan = csi + '36;1m'
end = csi + '0m'

cmd_alt = 'command' if system() == 'Darwin' else 'alt'

print('\nHello! My name is 16Bot, made by a lazy CS & Physics major named Shamith Pasula.')
print('I will be doing your 16A or 16B self-grade for you, giving you 8/10 on random questions to not be sus.')
print('The comments for the 8/10 questions are in data.json, edit them if you wish.')
print('If this isn\'t your first time meeting me and you want to update your data, delete data.json and run faster_grade.py again.')
print('If you mess up or want to restart, press Ctrl+C and run faster_grade.py again. \n')

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
    url = f'http://www.eecs{data_dict["class"]}.org/self-grade-{hw_number}.html'
    browser.visit(url)
    browser.find_by_id('name').fill(data_dict['name'])
    browser.find_by_id('email').fill(data_dict['email'])
    browser.find_by_id('sid').fill(data_dict['sid'])
    close()

    if data_dict['class'] == '16b':
        browser.find_by_value(resubmission).click()

    pyautogui.keyDown(cmd_alt)
    pyautogui.press('tab')
    pyautogui.keyUp(cmd_alt)

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

    pyautogui.keyDown(cmd_alt)
    pyautogui.press('tab')
    pyautogui.keyUp(cmd_alt)
    
    q, r = divmod(num_incorrects, len(data_dict['comments']))
    comments = q * data_dict['comments'] + data_dict['comments'][:r]

    for i in indices[:-num_incorrects]:
        browser.find_by_value('10')[i].click()

    counter = 0
    for i in indices[-num_incorrects:]:
        browser.find_by_value('8')[i].click()
        pyautogui.keyDown('tab')
        pyautogui.write(comments[counter])
        counter += 1

        
    browser.find_by_id('d' + difficulty).click()
    browser.find_by_id('Hours Spent').fill(hours_spent)
    browser.find_by_id('Teammate Headcount').fill(num_teammates)
    browser.find_by_id(went_to_hw_party).click()
    browser.find_by_xpath('/html/body/section/form/p/button').click()
    browser.find_by_id('json-download').click()

    sleep(3)

print()
print('Submit the downloaded .json file to Gradescope and you\'re done! Have a great day!')