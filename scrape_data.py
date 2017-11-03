from bs4 import BeautifulSoup
import requests
import dateparser
import datetime as dt
import json
from collections import defaultdict

page = requests.get('http://www.econtalk.org/archives.html')

soup = BeautifulSoup(page.text)

table = soup.find("table", attrs=dict(border="1", 
                        cellspacing="2",
                        cellpadding="2",
                        width="100%"))

headings = [th.get_text() for th in table.find("tr").find_all("th")]

data = defaultdict(lambda: defaultdict(dict))
for row in table.find_all("tr")[1:]:
    date, episode, _ = row.find_all("td")
    links = episode.find_all("a")
    if len(links):
        date = dateparser.parse(date.text)
        data[int(date.month)][int(date.day)][int(date.year)] = (links[0].text, links[0].attrs['href'])

with open("econtalk.json", 'w') as f:
    json.dump(data, f)