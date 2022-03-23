# EECS 16A/16B Self-Grade Bot (16Bot)

### For lazy 16AB students who don't want to do their weekly self-grade after spending 30 hours on the homework

## DISCLAIMER: faster vs easy

easy.py is an easy and fast alternative to the official EECS self-grade website, saving you the time and effort it takes to use that site. This self-grade method is _totally safe_ and allows you to complete it yourself.

faster.py is a __slightly unethical__ alternative which takes a very short amount of time by __randomly assigning 8's and 10's to your questions__. Be careful when using this, because you will not actually be grading your work; you will just be BS'ing self-grades because they are boring. While this is tempting, understand what you're getting into and that you are liable for any consequences of using this software. It is also highly recommended you at least look at the solutions before using this program so that you learn from any mistakes you made.

---------
Instructions:

Clone the repo:

`git clone https://github.com/shamith09/eecs16b-selfgrade-bot.git`

Go into the repo folder:

`cd eecs16bot`

Install Python and pip if you haven't already:

https://www.python.org/downloads/

https://pip.pypa.io/en/stable/installation/

---------
Setup using:

`make setup`

Run the program using:

`make grade`

---------
If make doesn't work, use:

`pip install -r bin/requirements.txt` to setup and
`python3 src/main.py` to run.

---------
To edit your data (email, 16A vs 16B, etc.) open data.json and change the data as you wish, or alternatively, delete data.json using:

`rm -rf bin/data.json`

and run main.py again so that 16Bot can ask you for your information again.
