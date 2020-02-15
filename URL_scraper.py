'''
This scraper was originally built as part of class assignment to scrape URLs 
from https://www.census.gov/programs-surveys/popest.html
'''

#Imports
from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse
import sys as s
import time
import csv

#########################################################################
# CAPTURE TARGET URL & DOMAIN FROM USER
#########################################################################
url = input("What URL should we scrape? ")
type(url)

#Handling exceptions/errors
proceed = input("You entered: " + str(url) + ", is this correct (Y or N)? ")
if proceed in ['y','Y']:
	print("URL saved")
elif proceed in ['n','N']:
	print("Please rerun and enter a valid URL and confirm with 'y' or 'Y' \n")
	s.exit(0)
else:
	print("Input not understood, exiting! \n")
	s.exit(0)

#Verify root level domain for conversion of absolute links
domain = input("Please verify root domain (ex. www.census.gov): ")
type(domain)

proceed = input("You entered: " + str(domain) + ", is this correct (Y or N)? ")
if proceed in ['y','Y']:
	print("Entering scrape phase...")
elif proceed in ['n','N']:
	print("Please rerun and enter a valid root domain and confirm with 'y' or 'Y' \n")
	s.exit(0)
else:
	print("Input not understood, exiting! \n")
	s.exit(0)

##############################################################################    
# BEGIN MAIN PROGRAM...									
##############################################################################
#Package request, send & catch response in single command
r = requests.get(url) 

#Extract response as HTML
html_doc = r.content

#Create BeautifulSoup object
soup = BeautifulSoup(html_doc,'lxml')
pretty_soup = soup.prettify

#########################################################################
# SAVE HTML TO LOCAL FILE
#########################################################################

html_filename = time.strftime("HTML-%Y%m%d-%H%M%S.html")
with open(html_filename, "w") as file:
	file.write(str(html_doc))

#########################################################################
# EXTRACT LINKS
#########################################################################

a_tags_all = soup.find_all("a")

#Print hrefs & text to screen
#for i in a_tags_all:
#	print("<a href='%s'>%s</a>" % (i.get("href"), i.text))

#########################################################################
# EVALUATE FOR LOCATOR TO HTML PAGE
#########################################################################

#Pass & clean 'a' tags to raw_link list
raw_links = []
for i in a_tags_all:
	#Clean refs starting w/ # or None
	if any ([(str(i.get("href")).startswith('#')), (str(i.get("href")).startswith('None'))]):
		pass
	else:	
		raw_links.append(i.get("href"))
	#print("Extracted raw URL is: " + str(i.get("href")))

print("Raw list has " + str(len(raw_links)) + " links!")

#########################################################################
# RELATIVE LINK TO ABSOLUTE
#########################################################################

#domain = "www.census.gov" #AUTOMATE THIS LATER

alt_absolute = []
for i in raw_links:
	p = urlparse(str(i), 'https')
	if p.netloc:
	    netloc = p.netloc
	    path = p.path
	else:
	    netloc = p.path
	    path = ''

	if not netloc.startswith('www.'):
		netloc = domain + netloc

	p = p._replace(netloc=netloc, path=path)
	#print(p.geturl())
	alt_absolute.append(p.geturl())

print("Absolute list has " + str(len(alt_absolute)) + " links!")

#########################################################################
# DEDUPLICATE LINKS
#########################################################################

dedup_links = []
for i in alt_absolute:
	if i not in dedup_links:
		dedup_links.append(i)
		#print(i)

print("Deduplicated list has " + str(len(dedup_links)) + " links!")

#########################################################################
# SAVE OUTPUT TO CSV FILE
#########################################################################
# https://wgu.hosted.panopto.com/Panopto/Pages/Viewer.aspx?id=45c6cc9e-f993-4580-a046-a8a701005b7d

csv_filename = time.strftime("links-%Y%m%d-%H%M%S.csv")
with open(csv_filename, "w", newline='') as f:
	cw = csv.writer(f, delimiter = ',')
	cw.writerows([i] for i in dedup_links)
	f.close

