import urlparse
import urllib
from bs4 import BeautifulSoup
from pprint import pprint
import requests

url = "http://www.nytimes.com/"

urls = [url]
visited = [url]

while len(urls) > 0:

    current_url  = urls.pop(0)
    try:
        htmltext = urllib.urlopen(current_url.read())
    except:
        print current_url
        continue
    soup = BeautifulSoup(htmltext)


    print len(urls)
    for tag in soup.findAll('a', href = True):
        tag['href'] = urlparse.urljoin(url, tag['href'])
        if url in tag['href'] and tag['href'] not in visited:
            urls.append(tag['href'])
            visited.append(tag['href'])

pprint(visited)