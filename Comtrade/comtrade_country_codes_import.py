from bs4 import BeautifulSoup
import xml_parse

soup = BeautifulSoup(open('/Users/tom/Desktop/CountryList.xml'), 'xml')
tag = soup.r
country = []
dictionary = xml_parse.get_names(tag, country)
df = xml_parse.to_frame(soup, dictionary)
xml_parse.to_unicode(df, 'utf-8')

