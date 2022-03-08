# EECS 16B Self-Grade Bot (16Bot)

### For lazy EECS/CS students who don't want to do their weekly self-grade after spending 30 hours on the homework

Instructions:

Clone the repo:

`git clone https://github.com/shamith09/eecs16b-selfgrade-bot.git`

Go into the repo folder:

`cd eecs16b-selfgrade-bot`

Install Python:
https://www.python.org/downloads/

---------
### Optional: Use a virtual environment to keep dependencies in the cloned repository:
Install virtualenv:

`pip install virtualenv`

Initialize the virtualenv and activate it:

`python3 -m venv env
source env/bin/activate`

---------

Install requirements:

`pip install -r requirements`

Follow instructions on the Splinter website to install the Chrome webdriver:
https://splinter.readthedocs.io/en/latest/drivers/chrome.html

Run main.py:

`python3 main.py`

DO NOT touch the keyboard or mouse when 16Bot tells you not to. 16Bot controls your computer when self-grading, so if you mess it up, it may do random stuff on your computer. It's unlikely this will cause serious damage to your computer, but please listen to 16Bot.

If you want to uninstall all the required dependencies that were installed, run:

`pip uninstall -r requirements -y`
