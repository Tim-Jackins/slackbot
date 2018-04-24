# Table of Contents
- [Background](#background)
- [Setup](#setup)
	- [Install](#install)
	- [Credentials](#credentials)
- [Code](#code)
- [Running](#running)

# Background
This was my attempt to make a simple python3 slack bot that would post our rank in zero robotics. At the time that I made this I didn't know how to use JavaScript and there's now [a better 'serverless' way to do this](https://github.com/johnagan/serverless-slackbot) which I would recommend checking out.

# Setup
## Install
Clone this repo:
```bash
git clone https://github.com/Tim-Jackins/zrbot.git
```

Next install the required packages
```bash
sudo -H pip3 install --trusted-host pypi.python.org -r requirements.txt
```
Ok, you're ready to move to the next step!

## Credentials

In order for the bot you make to communicate with your slack you have to give it some security credentials. These can be obtained in your slack. First go to apps menu by click on apps:

![fig1](media/slack_home.png)

Then click on the manage apps button in the top left part of the screen:

![fig2](media/manage_apps.png)

Then click on custom integrations, then bots, then "Add Configuration":

![fig3](media/integrations.png)

Then type a username (don't worry it can be changed later) and click "Add bot integration": 

![fig4](media/config.png)


Once you have your token and bot id lets save those as evironment variables:
```bash
export SLACK_API_TOKEN={Your bots API token}
```
Next run the script print_bot_id.py and follow the instructions. This will give you the id for the bot which you will then need to to export:
```bash
export SLACK_BOT_ID={Your bots}
```

The benefit of exporting is to be able to share your code with people without giving them all of your tokens. Anyways, once you have your tokens you are ready to start your app!

# Code
The main body of code can be found in [`run.py`](run.py)

# Running
Now you should just be able to run the script.
```bash
python3 run.py
```
