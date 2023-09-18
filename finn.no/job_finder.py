from select import select
from winsound import Beep
import requests
from bs4 import BeautifulSoup as bs
from pprint import pprint
import urllib.request as urllib2
# import lxml
# from lxml import etree, html

my_data = []

# url = 'https://www.finn.no/job/fulltime/search.html?published=1&q=biologi&sort=RELEVANCE'
# data = requests.get(url)
# soup = bs(data.text, 'html.parser')

parser = 'lxml'  # or 'lxml' (preferred) or 'html5lib', if installed
resp = urllib2.urlopen("https://www.finn.no/job/fulltime/search.html?published=1&q=utvikler&sort=RELEVANCE")
soup = bs(resp, parser, from_encoding = resp.info().get_param('charset'))

results = soup.find_all('div', class_ = 'ads__unit__content')

# bread = soup.find_all('div', class_ = 'ads__unit__content__keys')

# print(type(results))
# print(results)


for a in results:

    tittel = a.find('a', class_ = 'ads__unit__link')
    beskrivelse = a.find('div', class_ = 'ads__unit__content__keys')
    sted = a.find('div', class_ = 'u-stone')
    bedrift = a.find('div', class_ = 'ads__unit__content__list')
    link = a.find('a', href=True)['href']
        
    my_data.append({"tittel": tittel.text.strip(), "sted": sted.text.strip(), "bedrift": bedrift.text.strip(), "link": link})

    if beskrivelse != None: my_data.append({"beskrivelse": beskrivelse.text.strip()})

pprint(my_data)

