import os
from slackclient import SlackClient

BOT_NAME = input('What is your bot\'s name?: ')

slack_client = SlackClient(os.environ['SLACK_API_TOKEN'])

BOT_ID = ''

if __name__ == "__main__":
	api_call = slack_client.api_call('users.list')
	if api_call['ok']:
		# retrieve all users so we can find our bot
		for user in api_call['members']:
			if user['profile']['real_name'] == BOT_NAME:
				print('Bot ID for \'' + user['profile']['real_name'] + '\' is ' + user['id'])
				BOT_ID = user['id']
	else:
		print("could not find bot user with the name " + BOT_NAME)