from bs4 import BeautifulSoup
import pandas as pd
import lxml
import urllib2
from xml_parse import get_names

soup = BeautifulSoup(open('Comtrade.xml'), 'lxml')
tag = soup.r

# Refactor this to separate module.
# names = get_names(tag)
names = []
dictionary = get_names(tag, names)
tags = soup.findAll('r')

for key in dictionary.keys():
    for tag in tags:
        dictionary[key].append(tag.find(key).string)

df = pd.DataFrame(dictionary)

############ From the Web ############

xml = 'http://comtrade.un.org/ws/'
xmlpath = 'get.aspx?cc=TOTAL&px=H2&r=372&y=2006&comp=false&code='
access_code = '0+eQr1v/Ipy4z+k0Gbpgb7uR4roBFhizAELaCTsNqaRbSu5koYjlZSXNnj01N5Jq+qM/zN43pjkOtPV8EM1bi7p3JHZH7G221VQUoqJx0QO+LZ2QtYWVJ9tTgriP0b358hnSlo7DqWSizp4J1bIj6Mw9NQe5Pa85q6636s62AIA='

soup = BeautifulSoup(urllib2.urlopen(
        xml + xmlpath + access_code), 'lxml')