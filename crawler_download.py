import urlparse
import urllib2
from bs4 import BeautifulSoup
from pprint import pprint
import os
import sys
import re
import time

def check_if_first(elem,list_of_tuples):
    for x,y in list_of_tuples:
        if elem == x:
            return True
    return False

start_time = time.time()

# Useless here...
url_validation_regex = regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

# url = raw_input("[+] Enter the url: ")
# url = re.sub(r'#\S*',"", url)
# course_name = raw_input("[+] Enter the course name: ")
# complete_path = "/home/deyan/Desktop/KNOWLEDGEBASE/" + course_name
# if not os.path.exists(complete_path):
#     os.makedirs(complete_path)
#print(complete_path)
print ""

urls = [(url, "Main_Page")]
visited = [(url, "Main_Page")]
not_qualified = []
number_not_qualified = 0
number_qualified = 1
number_invalid = 0
invalid_pages = []
iteration = 1

try:
    connection_initial_url = urllib2.urlopen(url)
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

    try:
        connection =  urllib2.urlopen(urls[0][0])
        code_page = connection.getcode()
        if code_page >= 400:
            invalid_pages.append(urls[0])
            number_invalid += 1
            print "Tag invalid!"
            urls.pop(0)
            iteration += 1
            continue
        htmltext = connection.read()
        soup = BeautifulSoup(htmltext, "html.parser")
    except:
        print("Tag invalid!")
        invalid_pages.append(urls[0])
        number_invalid += 1
        urls.pop(0)
        iteration += 1
        continue

    current_url = urls.pop(0)
    extension = os.path.splitext(os.path.basename(current_url[0]))[1]
    if iteration > 1:
        if current_url not in visited:
            visited.append(current_url)
            number_qualified += 1
        else:
            continue


    print "On page %s right now" %(current_url[0])
    print "Extension: %s" %(extension)
    print "Getting links from the page..."

    for tag in soup.findAll('a', href = True):
        print "=========================="
        if tag['href'].startswith("www."):
            not_qualified.append((tag['href'],tag.text))
            number_not_qualified += 1
            print "Tag not qualified!"
            continue

        tag['href'] = urlparse.urljoin(current_url[0], tag['href'])
        tag['href'] = re.sub(r'#\S*', "", tag['href'])
        tag['href'] = tag['href'].strip()
        tag['href'].strip()
        print("Current page %s" %current_url[0])
        print "Tag %s" %tag['href']
        if check_if_first(tag['href'], visited) or check_if_first(tag['href'], not_qualified) or check_if_first(tag['href'],invalid_pages):
            print "Tag already assessed!"
            continue

        if url in tag['href'] and not check_if_first(tag['href'],visited):
            urls.append((tag['href'],tag.text))
            print "Tag qualified!"

        else:
            not_qualified.append((tag['href'],tag.text))
            number_not_qualified += 1
            print "Tag not qualified!"

    print("Elements in queue: %d" % len(urls))
    print"All links from page retrieved."
    print ""
    print "=========================="

    iteration += 1

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
print len(visited)
print "Time elapsed: {0} hours: {1} minutes: {2} seconds".format(hours_elapsed, formatted_minutes, formatted_seconds)


