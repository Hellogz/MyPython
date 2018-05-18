import requests
from bs4 import BeautifulSoup
import os


"""
pip install requests
pip install beautifulsoup4
pip install lxml
"""

url = "http://t66y.com/thread0806.php?fid=7"
title_tag = 'h3'

def get_from_file(filename):
	with open(filename, 'r') as f:
		r = f.read()
	return r

def get_title_link_from(url):
	r = requests.get(url)
	soup = BeautifulSoup(r.text, 'lxml')
	with open('test.txt', 'a', encoding='iso8859-1') as f:
		for link in soup.find_all(title_tag):
			f.write(link.string + ' http://t66y.com/' + link.a.get('href') + '\n')

def save_html_to_file(url, filename):
	data = requests.get(url).text
	with open(filename, 'a', encoding='iso8859-1') as f:
		f.write(data)	

def main():
	get_title_link_from(url)
	print("Save Done.")

if __name__ == '__main__':
	main()
	os.system("pause")
