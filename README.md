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

## faster vs easy

easy.py is an easy and fast alternative to the official EECS self-grade website, saving you the time and effort it takes to use that site. This self-grade method is _totally safe_ and allows you to complete it yourself.

faster.py is a __slightly unethical__ alternative which takes a very short amount of time by randomly assigning 8's and 10's to your questions. Be careful when using this, because you will not actually be grading your work; you will just be BS'ing self-grades because they are boring. While this is tempting, understand what you're getting into and that you are liable for any consequences of using this software. It is also highly recommended you at least look at the solutions before using this program so that you learn from any mistakes you made.

Run faster.py or easy.py:

`python3 faster.py` or `python3 easy.py`

DO NOT touch the keyboard or mouse when 16Bot tells you not to. 16Bot controls your computer when self-grading, so if you mess it up, it may do random stuff on your computer. It's unlikely this will cause serious damage to your computer, but please listen to 16Bot.

If you want to uninstall all the required dependencies that were installed, run:

`pip uninstall -r requirements -y`

---------
To edit your data (email, 16A vs 16B, etc.) open data.json and change the data as you wish, or alternatively, delete data.json using:

`rm -rf data.json`

and run faster_grade.py again so that 16Bot can ask you for your information again.
