from bs4 import BeautifulSoup
import pandas as pd
import lxml.html
import urllib2
from xml_parse import get_names

soup = BeautifulSoup(open('Comtrade.xml'), 'xml')
tag = soup.r

# Refactor this to separate module.
# names = get_names(tag)
names = []
for i in range(len(tag.findChildren())):
names.append(tag.findChildren()[i].name)
values = [list([]) for _ in range(len(names))]
dictionary = dict(zip(names, values))

tags = soup.findAll('r')

for key in dictionary.keys():
    for tag in tags:
        dictionary[key].append(tag.find(key).string)

df = pd.DataFrame(dictionary)

############ From the Web ############

# file = lxml.html.parse(url)
# url = 'http://comtrade.un.org/ws/get.aspx?px=H1&r=381&y=2003,2002&cc=TOTAL&p=0&comp=false'
# or? html = urllib2.urlopen(url)
