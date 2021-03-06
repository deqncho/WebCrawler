import urlparse
import urllib2
from bs4 import BeautifulSoup
from pprint import pprint
import os
import sys
import re
import time
import pdfkit

"""TODO - fix the structure of the file system outputed"""

def check_if_first(elem,list_of_tuples):
    for x,y in list_of_tuples:
        if elem == x:
            return True
    return False

# Useless here...
url_validation_regex = regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

url = raw_input("[+] Enter the url: ")
start_time = time.time()
url = re.sub(r'#\S*',"", url)
course_name = raw_input("[+] Enter the course name: ")
current_dir = "/home/deyan/Desktop/KNOWLEDGEBASE/" + course_name
if not os.path.exists(current_dir):
    os.makedirs(current_dir)
#print(complete_path)
print ""

urls = [(url, "Main_Page_Course")]
visited = [(url, "Main_Page_Course")]
not_qualified = []
number_not_qualified = 0
number_qualified = 1
number_invalid = 0
invalid_pages = []
iteration = 1
links_for_page = []
links_added = False

try:
    connection_initial_url = urllib2.urlopen(url)
    code_initial_url = connection_initial_url.getcode()
    html_initial = connection_initial_url.read()
    if code_initial_url >= 400:
        print "Invalid initial URL!"
        print "Exiting..."
        sys.exit(0)

    basename = os.path.basename(url)
    extension_initial = os.path.splitext(basename)[1]
    if extension_initial not in ['','.html']:
        print "\n[*] Downloading: %s" % (os.path.basename(url))
        path = current_dir + "/" + os.path.basename(url)
        print(path)
        with open(path, 'wb') as f:
            f.write(html_initial)
    else:
        if not links_added:
            os.makedirs(os.path.normpath(os.path.join(current_dir, urls[0][1])))
        else:
            print "\n[*] Downloading: .html"

            current_dir = os.path.normpath(os.path.join(current_dir, urls[0][1]))
            # os.makedirs(current_dir)
            print(current_dir)
            path = current_dir + "/" + urls[0][1]
            print(path)
            with open(path, 'wb') as f:
                f.write(html_initial)
        # print "\n[*] Downloading: .html"
        # path = current_dir + "/" + urls[0][1]
        # print(path)
        # with open(path, 'wb') as f:
        #     f.write(html_initial)

except Exception as e:
    print e
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
    basename_current = os.path.basename(current_url[0])
    print basename_current
    extension_current = os.path.splitext(basename_current)[1]

    if iteration > 1:
        if current_url not in visited:

            if len(links_for_page) == 0:
                links_added = False
            elif links_added:
                links_for_page.pop(0)
                if len(links_for_page) == 0:
                    links_added = False

            if extension_current not in ['','.html']:

                print "\n[*] Downloading: %s" % (current_url[1])
                path_current = current_dir + "/" + os.path.basename(current_url[0])
                print(path_current)
                with open(path_current, 'wb') as f:
                    f.write(htmltext)
            else:
                if not links_added:
                    os.makedirs(os.path.normpath(os.path.join(current_dir,current_url[1])))
                else:
                    print "\n[*] Downloading: .html"

                    current_dir = os.path.normpath(os.path.join(current_dir,current_url[1]))
                    #os.makedirs(current_dir)
                    file_to_create = current_dir + "/" + "Sub_Page"
                    print(file_to_create)
                    with open(file_to_create, 'wb') as f:
                        f.write(htmltext)
            print '**************'
            print links_for_page
            print '**************'

            visited.append(current_url)
            number_qualified += 1

        else:

            continue


    # elif extension_current in ['', '.html']:
    #     print(current_url)
    #     bla = complete_path + "/" + current_url[1]
    #     pdfkit.from_url(current_url[0], complete_path + "/" + current_url[1])


    print "On page %s right now" %(current_url[0])
    print "Extension: %s" %(extension_current)
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
            if not links_added:
                links_for_page.append(tag['href'])
            print "Tag qualified!"

        else:
            not_qualified.append((tag['href'],tag.text))
            number_not_qualified += 1
            print "Tag not qualified!"

    print("Elements in queue: %d" % len(urls))
    print"All links from page retrieved."
    print ""
    print "=========================="
    if not links_added:
        links_added = True
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
print "Time elapsed after input: {0} hours: {1} minutes: {2} seconds".format(hours_elapsed, formatted_minutes, formatted_seconds)


