import urlparse
import urllib
from bs4 import BeautifulSoup
from pprint import pprint
import os

url = raw_input("[+] Enter the url: ")
course_name = raw_input("[+] Enter the course name: ")
complete_path = "/home/deyan/Desktop/KNOWLEDGEBASE/" + course_name
if not os.path.exists(complete_path):
    os.makedirs(complete_path)
print(complete_path)

urls = [url]
visited = [url]

while len(urls) > 0:
    try:
        htmltext = urllib.urlopen(urls[0]).read()
    except:
        print urls[0]
    soup = BeautifulSoup(htmltext)
    
    current_url = urls.pop(0)
    extension = os.path.splitext(os.path.basename(current_url))[1]
    print "On page %s right now" %(current_url)
    print "Extension: %s" %(extension)
    print "========================="

    print(len(urls))

    for tag in soup.findAll('a', href = True):
        tag['href'] = urlparse.urljoin(url, tag['href'])
        if url in tag['href'] and tag['href'] not in visited:
            urls.append(tag['href'])
            visited.append(tag['href'])
            print(tag['href'])