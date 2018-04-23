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

What follows is a template for building your app. Feel free to copy it down and leave now but if it looks weird countinue down and I will step through it.

```python
import os
import time
import pprint
import slackclient as sc
import re

BOT_ID = os.environ['SLACK_BOTID']
AT_BOT = '<@' + BOT_ID + '>'
pp = pprint.PrettyPrinter(indent=4)
slack_client = sc.SlackClient(os.environ['SLACK_API_TOKEN'])
MENTION_REGEX = '^<@(|[WU].+?)>(.*)'

def handle_command(text, channel, raw_output):
	if text.startswith('hello'):
		response = 'Well hello there <@{0}>'.format(raw_output['user']) 
	elif 'info' in text:
		response = ''
		for cell in raw_output:
			if cell == 'user':
				response += '{0}: <@{1}>\n'.format(cell, raw_output[cell])
			else:
				response += '{0}: {1}\n'.format(cell, raw_output[cell].replace('@', ''))
	else:
		response = 'Say "hello" to chat with me! Or ask for some info.'
	slack_client.api_call(
		"chat.postMessage",
		channel=channel,
		text=response,
		as_user=True)
	print('Command handled')
def parse_slack_output(slack_rtm_output):
	output_list = slack_rtm_output
	if output_list and len(output_list) > 0:
		for output in output_list:
			pp.pprint(output)
			try:
				matches = re.search(MENTION_REGEX, output['text'])
				if matches:
					# the first group contains the username (matches.group(1)), the second group contains the remaining message
					return matches.group(2).strip(), output['channel'], output
			except:
				pass
	return None, None, None
if __name__ == "__main__":
	READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
	if slack_client.rtm_connect():
		print("StarterBot connected and running!")
		while True:
			command, channel, raw_output = parse_slack_output(slack_client.rtm_read())
			if command and channel:
				print(command)
				if handle_command(command, channel, raw_output):
					break
			time.sleep(READ_WEBSOCKET_DELAY)
	else:
		print("Connection failed. Invalid Slack token or bot ID?")
print("Bot turned off")
```

## Imports
```python
import os			# Used for running terminal commands
import time			# Has handy functions relating to time
import pprint			# Includes a function for printing dictionaries nicely
import slackclient as sc	# The slack api we'll use to talk to the workspace
import re			# Using regex in python
```

## Initializing
It's self explanatory; however, if you don't know what regular expressions are: [Link 1](https://www.regular-expressions.info/) [Link 2](https://regexr.com/)
```python
BOT_ID = os.environ['SLACK_BOTID']				# Get your slack token
AT_BOT = '<@' + BOT_ID + '>'					# How the mention from slack will appear to the bot
pp = pprint.PrettyPrinter(indent=4)				# Initialize the dictionary printer
slack_client = sc.SlackClient(os.environ['SLACK_API_TOKEN'])	# Initialize the slack client
MENTION_REGEX = '^<@(|[WU].+?)>(.*)'				# This is regex for matching slack mentions
```

## Handling commands
This command is for deciding what the response should be and then making the api call
```python
def handle_command(text, channel, raw_output):
	if 'hello' in text:
		response = 'Well hello there <@{0}>'.format(raw_output['user']) 
	elif 'info' in text:
		response = ''
		for cell in raw_output:
			if cell == 'user':
				response += '{0}: <@{1}>\n'.format(cell, raw_output[cell])
			else:
				response += '{0}: {1}\n'.format(cell, raw_output[cell])
	else:
		response = 'Say "hello" to chat with me! Or ask for some info.'
	slack_client.api_call(
		"chat.postMessage",
		channel=channel,
		text=response,
		as_user=True)
	print('Command handled')
```

## Parsing the output
This uses the MENTION_REGEX string to figure out if a person was talking to the bot.
```python
def parse_slack_output(slack_rtm_output):
	output_list = slack_rtm_output
	if output_list and len(output_list) > 0:
		for output in output_list:
			pp.pprint(output)
			try:
				matches = re.search(MENTION_REGEX, output['text'])
				if matches:
					# the first group contains the username (matches.group(1)), the second group contains the remaining message
					return matches.group(2).strip(), output['channel'], output
			except:
				pass
	return None, None, None
```

## Main
Pretty simple. Wait till something is texted then check to see if it mentions the bot.
```python
if __name__ == "__main__":
	READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
	if slack_client.rtm_connect():
		print("StarterBot connected and running!")
		while True:
			command, channel, raw_output = parse_slack_output(slack_client.rtm_read())
			if command and channel:
				print(command)
				if handle_command(command, channel, raw_output):
					break
			time.sleep(READ_WEBSOCKET_DELAY)
	else:
		print("Connection failed. Invalid Slack token or bot ID?")
print("Bot turned off")
```

# Running
Now you should just be able to run the script.
```bash
python3 run.py
```
