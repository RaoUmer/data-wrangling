from bs4 import BeautifulSoup
from xml_parse import get_names, to_frame

soup = BeautifulSoup(open('/Users/tom/Desktop/CountryList.xml'), 'xml')
tag = soup.r
country = []
dictionary = get_names(tag, country)
df = to_frame(soup, dictionary)

for column in df.columns:
	for row in range(len(df.iso2)):
	    try:
	        df[column][row] = df[column][row].encode('utf-8')
	    except:
	        print row, df[column][row]
