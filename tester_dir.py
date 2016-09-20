import urlparse
import urllib2
from bs4 import BeautifulSoup
from pprint import pprint
import os
import sys
import re
import time
import pdfkit

def check_connection(url):
    try:
        connection_initial_url = urllib2.urlopen(url)
        code_initial_url = connection_initial_url.getcode()
        resource = connection_initial_url.read()
        if code_initial_url >= 400:
            print "Invalid initial URL!"
            print "Exiting..."
            sys.exit(0)
        return connection_initial_url, resource

    except:
        print "Invalid initial URL!"
        print "Exiting..."
        sys.exit(0)

def check_if_first(elem,list_of_tuples):
    for x,y in list_of_tuples:
        if elem == x:
            return True
    return False


def get_input():
    url = raw_input("[+] Enter the url: ")
    url = re.sub(r'#\S*', "", url)
    course_name = raw_input("[+] Enter the course name: ")
    complete_path = "/home/deyan/Desktop/KNOWLEDGEBASE/" + course_name
    if not os.path.exists(complete_path):
        os.makedirs(complete_path)
    print ""
    return url, complete_path

def get_basename(url):
    return os.path.basename(url)

def get_extension(basename):
    return os.path.splitext(basename)[1]

def process_first_page(url, path_to_course, resource, main_page):
    try:
        basename = get_basename(url)
        extension_initial = get_extension(basename)
        if extension_initial not in ['', '.html']:
            print "\n[*] Downloading: %s" % (basename)
            path = path_to_course + "/" + basename
            print(path)
            with open(path, 'wb') as f:
                f.write(resource)
        else:
            print "\n[*] Downloading: %s" % (basename)
            path = path_to_course + "/" + main_page.replace('/', '-')
            print(path)
            with open(path, 'wb') as f:
                f.write(resource)

                # elif extension_initial in ['', '.html']:
                #     pdfkit.from_url(url,complete_path + "/" + urls[0][1])
    except Exception as e:
        print e
        print "Couldn't download initial page!"
        print "Exiting..."
        sys.exit(0)

def main():

    start_time = time.time()
    url, path_to_course = get_input()

    # print(complete_path)
    main_page = "Main_Page.html"
    urls = [(url, main_page)]
    visited = [(url, main_page)]
    not_qualified = []
    number_not_qualified = 0
    number_qualified = 1
    number_invalid = 0
    invalid_pages = []
    iteration = 1
    links_for_page = []
    links_added = False
    starting_link = ''
    starting_links = []

    connection_initial_url, resource = check_connection(url)

    process_first_page(url,path_to_course,resource,main_page)

    while len(urls) > 0:

        try:
            connection = urllib2.urlopen(urls[0][0])
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
        #1
        current_url = urls.pop(0)
        basename_current = os.path.basename(current_url[0])
        print basename_current
        extension_current = os.path.splitext(basename_current)[1]

        if iteration > 1:
            if current_url not in visited:

                if len(links_for_page) == 0:
                    starting_link = current_url[0]
                    links_added = False
                else:
                    links_for_page.pop(0)

                print '****************'
                print starting_link
                print links_for_page
                print '****************'
                if extension_current not in ['', '.html']:
                    print "\n[*] Downloading: %s" % (current_url[1])
                    path_current = path_to_course + "/" + os.path.basename(current_url[0])
                    print(path_current)
                    with open(path_current, 'wb') as f:
                        f.write(htmltext)
                else:
                    print "\n[*] Downloading: %s" % (current_url[1])
                    path_current = path_to_course + "/" + current_url[1].replace('/', '-')
                    print(path_current)
                    with open(path_current, 'wb') as f:
                        f.write(htmltext)

                visited.append(current_url)
                number_qualified += 1


            else:
                continue

        # elif extension_current in ['', '.html']:
        #     print(current_url)
        #     bla = complete_path + "/" + current_url[1]
        #     pdfkit.from_url(current_url[0], complete_path + "/" + current_url[1])


        print "On page %s right now" % (current_url[0])
        print "Extension: %s" % (extension_current)
        print "Getting links from the page..."

        for tag in soup.findAll('a', href=True):
            print "=========================="
            if tag['href'].startswith("www."):
                not_qualified.append((tag['href'], tag.text))
                number_not_qualified += 1
                print "Tag not qualified!"
                continue

            tag['href'] = urlparse.urljoin(current_url[0], tag['href'])
            tag['href'] = re.sub(r'#\S*', "", tag['href'])
            tag['href'] = tag['href'].strip()
            tag['href'].strip()
            print("Current page %s" % current_url[0])
            print "Tag %s" % tag['href']
            if check_if_first(tag['href'], visited) or check_if_first(tag['href'], not_qualified) or check_if_first(
                    tag['href'], invalid_pages):
                print "Tag already assessed!"
                continue

            if url in tag['href'] and not check_if_first(tag['href'], visited):
                if not links_added:
                    links_for_page.append(tag['href'])
                urls.append((tag['href'], tag.text))
                print "Tag qualified!"

            else:
                not_qualified.append((tag['href'], tag.text))
                number_not_qualified += 1
                print "Tag not qualified!"

        print("Elements in queue: %d" % len(urls))
        print"All links from page retrieved."
        print ""
        print "=========================="
        links_added = True
        iteration += 1
        starting_links.append((starting_link,links_for_page))

    print ""
    print "Number of qualified pages: %d" % number_qualified
    pprint(visited)
    print "=========================="
    print ""
    print "Number of not qualified pages: %d" % number_not_qualified
    pprint(not_qualified)
    print "=========================="
    print ""
    print "Number of invalid pages %d" % number_invalid
    pprint(invalid_pages)
    print "=========================="
    print ""

    seconds_elapsed = int(time.time() - start_time)
    formatted_seconds = seconds_elapsed % 60
    minutes_elapsed = int(seconds_elapsed / 60)
    formatted_minutes = minutes_elapsed % 60
    hours_elapsed = int(minutes_elapsed / 60)
    print len(visited)
    print "Pages and their links: {}".format(starting_links)
    print "Time elapsed after input: {0} hours: {1} minutes: {2} seconds".format(hours_elapsed, formatted_minutes,
                                                                                 formatted_seconds)


if __name__ == "__main__":
    main()