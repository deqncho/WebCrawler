import urlparse
import urllib2
from bs4 import BeautifulSoup
from pprint import pprint
import os
import sys
import re
import time

start_time = time.time()

# Not used in the program so far...
# url_validation_regex = regex = re.compile(
#         r'^(?:http|ftp)s?://' # http:// or https://
#         r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
#         r'localhost|' #localhost...
#         r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
#         r'(?::\d+)?' # optional port
#         r'(?:/?|[/?]\S+)$', re.IGNORECASE)

url = raw_input("[+] Enter the url: ")
url = re.sub(r'#\S*',"", url)
# course_name = raw_input("[+] Enter the course name: ")
# complete_path = "/home/deyan/Desktop/KNOWLEDGEBASE/" + course_name
# if not os.path.exists(complete_path):
#     os.makedirs(complete_path)
# #print(complete_path)
# print ""

urls = [url]
visited = [url]
not_qualified = []
number_not_qualified = 0
number_qualified = 0
number_invalid = 0
invalid_pages = []

try:
    connection_initial_url = urllib2.urlopen(url, timeout=10)
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

    connection =  urllib2.urlopen(urls[0], timeout=10)
    htmltext = connection.read()
    soup = BeautifulSoup(htmltext, "html.parser")
    current_url = urls.pop(0)
    extension = os.path.splitext(os.path.basename(current_url))[1]
    print "On page %s right now" %(current_url)
    print "Extension: %s" %(extension)
    print "Getting links from the page..."

    for tag in soup.findAll('a', href = True):
        print "=========================="
        if tag['href'].startswith("www."):
            not_qualified.append(tag['href'])
            number_not_qualified += 1
            print "Tag not qualified!"
            continue

        tag['href'] = urlparse.urljoin(current_url, tag['href'])
        tag['href'] = re.sub(r'#\S*', "", tag['href'])
        tag['href'] = tag['href'].strip()
        tag['href'].strip()
        print("Current page %s" %current_url)
        print "Tag %s" %tag['href']
        if tag['href'] in visited or tag['href'] in not_qualified or tag['href'] in invalid_pages:
            continue
        try:
            connection_tag = urllib2.urlopen(tag['href'], timeout=10)
            code_tag = connection_tag.getcode()
            if code_tag >= 400:
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
    print ""
    print "=========================="

print ""
print "Number of qualified pages: %d" %number_qualified
pprint (visited)
print "=========================="
print ""
print "Number of not qualified pages: %d" % number_not_qualified
pprint(not_qualified)
print "=========================="
print ""
print "Number of invalid pages %d" %number_invalid
pprint(invalid_pages)
print "=========================="
print ""

seconds_elapsed = int(time.time() - start_time)
formatted_seconds = seconds_elapsed % 60
minutes_elapsed = int(seconds_elapsed / 60)
formatted_minutes = minutes_elapsed % 60
hours_elapsed = int(minutes_elapsed / 60)
print "Time elapsed: {0} hours: {1} minutes: {2} seconds".format(hours_elapsed, formatted_minutes, formatted_seconds)
