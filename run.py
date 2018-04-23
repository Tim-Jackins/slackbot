import os			# Used for running terminal commands
import time			# Has handy functions relating to time
import pprint			# Includes a function for printing dictionaries nicely
import slackclient as sc	# The slack api we'll use to talk to the workspace
import re			# Using regex in python

BOT_ID = os.environ['SLACK_BOTID']				# Get your slack token
AT_BOT = '<@' + BOT_ID + '>'					# How the mention from slack will appear to the bot
pp = pprint.PrettyPrinter(indent=4)				# Initialize the dictionary printer
slack_client = sc.SlackClient(os.environ['SLACK_API_TOKEN'])	# Initialize the slack client
MENTION_REGEX = '^<@(|[WU].+?)>(.*)'				# This is regex for matching slack mentions

def handle_command(text, channel, raw_output):
	if text.startswith('hello'):
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
