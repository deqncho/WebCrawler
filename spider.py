import urlparse
import urllib
from bs4 import BeautifulSoup
from pprint import pprint
import os
import sys

url = raw_input("[+] Enter the url: ")
course_name = raw_input("[+] Enter the course name: ")
complete_path = "/home/deyan/Desktop/KNOWLEDGEBASE/" + course_name
if not os.path.exists(complete_path):
    os.makedirs(complete_path)
#print(complete_path)
print ""

urls = [url]
visited = [url]
not_qualified = []
number_not_qualified = 0
number_qualified = 0
number_invalid = 0
invalid_pages = []

try:
    connection_initial_url = urllib.urlopen(url)
    code_initial_url = connection_initial_url.getcode()
    if code_initial_url >= 400:
        print "Invalid initial URL!"
        print "Exiting..."
        sys.exit(0)

except:
    print "Invalid initial URL!"
    print "Exiting..."
    sys.exit(0)


while len(urls) > 0:

    connection =  urllib.urlopen(urls[0])
    code = connection.getcode()
    htmltext = connection.read()
    soup = BeautifulSoup(htmltext, "html.parser")
    current_url = urls.pop(0)
    extension = os.path.splitext(os.path.basename(current_url))[1]
    print "On page %s right now" %(current_url)
    print "Extension: %s" %(extension)
    print "Getting links from the page..."

    for tag in soup.findAll('a', href = True):
        print "=========================="
        tag['href'] = urlparse.urljoin(current_url, tag['href'])
        print("Current page %s" %current_url)
        print "Tag %s" %tag['href']
        try:
            connection_tag = urllib.urlopen(tag['href'])
            code_tag = connection_tag.getcode()
            if code >= 400:
                invalid_pages.append(tag['href'])
                number_invalid += 1
                print "Tag invalid!"
                continue

        except:
            invalid_pages.append(tag['href'])
            number_invalid += 1
            print "Tag invalid!"
            continue

        if url in tag['href'] and tag['href'] not in visited:
            number_qualified += 1
            print "Tag qualified!"
            urls.append(tag['href'])
            visited.append(tag['href'])
        else:
            not_qualified.append(tag['href'])
            number_not_qualified += 1
            print "Tag not qualified!"

    print("Elements in queue: %d" % len(urls))
    print"All links from page retrieved."
    print "=========================="

print "Number of qualified pages: %d" %number_qualified
pprint (visited)
print "=========================="
print "Number of not qualified pages: %d" % number_not_qualified
pprint(not_qualified)
print "=========================="
print "Number of invalid pages %d" %number_invalid
pprint(invalid_pages)