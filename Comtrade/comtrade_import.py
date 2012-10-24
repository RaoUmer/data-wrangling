from bs4 import BeautifulSoup
import pandas as pd
# from xml_parse import get_names

soup = BeautifulSoup(open('Comtrade.xml'), 'xml')
tag = soup.r

# Refactor this to separate module.
# names = get_names(tag)
names = []
for i in range(len(tag.findChildren())):
names.append(tag.findChildren()[i].name)
values = [list([]) for _ in range(len(names))]
dictionary = zip(names, values)

# dict = {
#     'pfCode' : pfCode,
#     'yr' : yr,
#     'rgCode' : rgCode,
#     'rtCode' : rtCode,
#     'ptCode' : ptCode,
#     'cmdCode' : cmdCode,
#     'cmdID' : cmdID,
#     'qtCode' : qtCode,
#     'TradeQuantity' : TradeQuantity,
#     'NetWeight' : NetWeight,
#     'TradeValue' : TradeValue,
#     'estCode' : estCode,
#     'htCode' : htCode,
# }

tags = soup.findAll('r')

for key in dictionary.keys():
    for tag in tags:
        dictionary[key].append(tag.find(key).string)

df = pd.DataFrame(dictionary)
    