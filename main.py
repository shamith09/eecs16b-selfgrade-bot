from time import sleep
from splinter import Browser
from random import shuffle
import pyautogui

with Browser('chrome') as browser:
    # params
    hw_number = 5
    difficulty = 5
    num_incorrects = 7
    comments = ['Calculation error', 'Misread question']

    hours_spent = 4
    num_teammates = 0
    went_to_hw_party = False
    
    # code
    if hw_number < 10:
        hw_number = '0' + str(hw_number)
    else:
        hw_number = str(hw_number)
    difficulty = str(difficulty)
    went_to_hw_party = "Y" if went_to_hw_party else "N"

    url = f'http://www.eecs16b.org/self-grade-{hw_number}.html'
    browser.visit(url)
    browser.find_by_id('name').fill('Shamith Pasula')
    browser.find_by_id('email').fill('shamith09@berkeley.edu')
    browser.find_by_id('sid').fill(3036587074)
    browser.find_by_id('resubmission').click()

    inputs = browser.find_by_value('Comment')
    indices = list(range(len(inputs)))
    shuffle(indices)

    q, r = divmod(num_incorrects, len(comments))
    comments = q * comments + comments[:r]

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

    sleep(10)
