import requests			# Allows you to send HTTP/1.1 requests
from bs4 import BeautifulSoup	# BeautifulSoup is an awesome html parser that is useful to learn

team = input('Enter a 2017 ZR alliance team: ')
url = 'http://zerorobotics.mit.edu/tournaments/28/rank/100/0/'
html_content = requests.get(url).content.decode('utf-8').strip() # Get the html page with requests

leaderboard = BeautifulSoup(html_content, 'lxml').body.table # Get the first table from the body of the page

cells = [str(elem) for elem in leaderboard.find_all('td')] # Find all occurances of <td> tag

for i in range(len(cells)):
	if i % 5 == 0:
		if cells[i][64:-9] == team:
			print('{0}\'s rank is {1}'.format(team, int(i / 5) + 1))
