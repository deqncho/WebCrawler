import urlparse
import urllib2
import os
import sys
import requests

try:
    from bs4 import BeautifulSoup
except ImportError:
    print "[*] Please download and install BeautifulSoup first!"
    sys.exit(0)
url = raw_input("[+] Enter the url: ")
course_name = raw_input("[+] Enter the course name: ")
complete_path = "/home/deyan/Desktop/KNOWLEDGEBASE/" + course_name
if not os.path.exists(complete_path):
    os.makedirs(complete_path)
print(complete_path)

try:
    i = 0
    request = urllib2.Request(url, None)
    html = urllib2.urlopen(request)
    soup = BeautifulSoup(html.read()) # to parse the website
    for tag in soup.findAll('a', href = True):
        try:
            tag['href'] = urlparse.urljoin(url, tag['href'])
            print(tag['href'])
            extension = os.path.splitext(os.path.basename(tag['href']))[1]
        except:
            "Exception on parsing data!"
            continue
        print(extension)
        try:
            response = requests.get(tag['href'])
            if response.status_code >= 400:
                continue
        except:
            print("Exception on response from server!")
            continue
        if extension in ['.png','.jpg','.pdf','.tar.gz','.c','.scala','.jar','.hs','.py','.pl','.txt','.java','.m','.gz','.md','.gir','zip','.ogg']:

            current = urllib2.urlopen(tag['href'])
            print "\n[*] Downloading: %s" %(os.path.basename(tag['href']))
            path = complete_path + "/" + os.path.basename(tag['href'])
            print(path)
            f = open(complete_path + "/" + os.path.basename(tag['href']),'wb')
            f.write(current.read())
            f.close()
            i+=1
        else:
            continue
    print "\n[*] Downloaded %d files" %(i+1)
    raw_input("[+] Press any key to exit...")
except KeyboardInterrupt:
    print "[*] Exiting..."
    sys.exit(1)
except IndexError as e:
    print "Done!"
except urllib2.URLError as e:
    print "[*] Could not get information from server!!"
    sys.exit(2)
except:
    print "I don't know the problem but sorry!!"
    sys.exit(3)

print("All good!")