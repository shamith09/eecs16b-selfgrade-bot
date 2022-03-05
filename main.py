from fileinput import close
from time import sleep
from splinter import Browser
from random import shuffle
import pyautogui
import json

csi = '\x1B['
red = csi + '31;1m'
yellow = csi + '33;1m'
cyan = csi + '36;1m'
end = csi + '0m'

print('\nHello! I am the EECS 16B self-grade bot, made by a lazy CS & Physics major named Shamith Pasula.')
print('I will be doing your self-grade for you, giving you 8/10 on some questions to not be sus.')
print('The comments for the 8/10 questions are in main.py, edit them if you wish.')
print('If this isn\'t your first time meeting me and you want to update your data, delete data.json and run main.py again.')
print('If you mess up or want to restart, press Ctrl+C and run main.py again. \n')

data_dict = {}

def get_data():
    data_dict['name'] = input('What is your full name (First Last)? ').strip()
    data_dict['sid'] = int(input('What is your SID? ').strip())
    data_dict['email'] = input('What is your @berkeley.edu email?: ').strip()
    while (data_dict['email'][-13:] != '@berkeley.edu'):
        data_dict['email'] = input('Please enter a valid @berkeley.edu email address: ')
    print()

    with open('data.json', 'w') as data:
        data.write(json.dumps(data_dict))

# params
try:
    data_dict = open('data.json', 'r')
    data_dict = json.load(data_dict)
    print('I have your name, email, and SID already!')
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

        resubmission = None
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
    print(f'{cyan}A new Google Chrome window will open in a new window in {5 - i} seconds. Navigate back to your terminal once it opens to continue.{end}', end = '\r')
    sleep(1)
print('\nOpening now...')

with Browser('chrome') as browser:
    # code
    difficulty = str(difficulty)

    url = f'http://www.eecs16b.org/self-grade-{hw_number}.html'
    browser.visit(url)
    browser.find_by_id('name').fill(data_dict['name'])
    browser.find_by_id('email').fill(data_dict['email'])
    browser.find_by_id('sid').fill(data_dict['sid'])
    close()

    browser.find_by_value(resubmission).click()

    inputs = browser.find_by_value('Comment')
    indices = list(range(len(inputs)))
    shuffle(indices)

    print(f'There are {len(indices)} questions on this HW.')
    print()
    num_incorrects = int(input('How many questions out of these do you want to give an 8/10? ').strip())
    print('I will now do your self-grade for you! I\'ll mark random questions as 8/10 and the rest as 10/10.')
    print(yellow + '\nIMPORTANT: Please navigate back to the Chrome window in the next 5 seconds so I can do your self-grade!' + end)
    print(cyan + 'You can do this by using ⌘+Tab on Mac and Alt+Tab on Windows.' + end)


    print()
    for i in range(5):
        print(f'{cyan}Beginning self-grade in {5 - i} seconds.{end}', end='\r')
        sleep(1)
    print('\nSelf-grading now...')

    # EDIT THIS list TO ADD/CHANGE COMMENTS
    #
    # There is no limit to the number of comments you can add,
    # so add as many as you like!
    comments = ['Calculation error', 'Misread question']

    q, r = divmod(num_incorrects, len(comments))
    comments = q * comments + comments[:r]

    for i in indices[:-num_incorrects]:
        browser.find_by_value('10')[i].click()

    sleep(2)
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

print('Submit the downloaded .json file to Gradescope and you\'re done! Have a great day!')