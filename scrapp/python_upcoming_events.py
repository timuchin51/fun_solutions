from bs4 import BeautifulSoup
from urllib.request import urlopen


python_org_url = 'https://www.python.org/events/python-events'

html = urlopen(python_org_url)
soup = BeautifulSoup(html, features='html.parser')

