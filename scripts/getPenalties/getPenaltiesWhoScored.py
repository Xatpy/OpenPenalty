import urllib2, urlparse, string
import time

BASE_URL = "http://www.bdfutbol.com/es"

#import BeautifulSoup
#from BeautifulSoup import BeautifulSoup
from bs4 import BeautifulSoup


import urllib2
import threading

class MyHandler(urllib2.HTTPHandler):
    def http_response(self, req, response):
        print "url: %s" % (response.geturl(),)
        print "info: %s" % (response.info(),)
        for l in response:
            print l
        print "responseeeeeeee"
        return response

#o = urllib2.build_opener(MyHandler())
#t = threading.Thread(target=o.open, args=('http://www.google.com/',))
#t.start()
#print "I'm asynchronous!"


def get_page2(url):
    time.sleep(1.5)
    print 'url:', url
    try:
    	print "vamos"
        return urllib2.urlopen(url).read()
    except urllib2.HTTPError as err:
        print 'urllib2.HTTPError: \n\t url: %s \n\t err: %s' % (url, err)

def getPage(theURL):
  ## returns the HTML text of the URL
	#req = urllib2.Request(theURL)
	#thePage = urllib2.urlopen(req)
	#time.sleep(5)
	#theHTML = thePage.read()

	#print "theHTML " + theHTML

	#theHTML = urllib2.urlopen(theURL)
	#for line in theHTML:
	#	print line
	#print "hola"

	#o = urllib2.build_opener(MyHandler())
	#t = threading.Thread(target=o.open, args=(theURL,))
	#t.start()

	#soup = BeautifulSoup(urllib2.urlopen(theURL))
	#title_ret = soup.title.string

	
	#html = urllib2.urlopen("http://www.pythonscraping.com/exercises/exercise1.html")
	#bsObj = BeautifulSoup(html.read());
	#print(bsObj.h1)

	html = urllib2.urlopen(theURL)
	soup = BeautifulSoup(html.read())
	print(soup.h1)
	title_ret = soup.title.string
	#title_ret = ""
	return title_ret
	
	#return theHTML

def extractTitle(theLine):
	## finds and returns contents of <title> tag
	titleStart = theLine.find("<title>")
	#print "ey " + theLine
	if titleStart > -1: #make sure we found the tag, -1 will mean we did not
		titleStart = titleStart + 7 #skip to end of tag
		titleEnd = theLine.find("</title>")
		theTitle = theLine[titleStart:titleEnd]
		theTitle = theTitle.strip() # remove whitespace
		print "vamossss"
	else:
		theTitle = ""
		print "joooo"
		
	return(theTitle)

def getNombrePartido(web):
	for line in web:
		if "</title>" in line:
			return line
	return ""


def checkPenalty(web):
	for line in web:
		if 'class="GP"' in line:
			return True
	return False


def processURL(url):
	web = urllib2.urlopen(url)
	web_aux = web
	ret = ""
	nombrePartido = getNombrePartido(web)
	title = extractTitle
	if checkPenalty(web):
		ret = nombrePartido
	return ret


def extractLinksFromLine(line):
    index = 0
    while index < len(line):
        index = line.find('/p/p.php?id=', index)
        if index == -1:
            break
        link = line[index:index+17] # +5 characters from the id
        link = BASE_URL + link
        partidoConPenaltis = processURL(link)
        if (partidoConPenaltis != ""):
        	print partidoConPenaltis
        	f.write(partidoConPenaltis)
        index += 12 # +2 because len(''/p/p.php?id=') == 2


def checkIfPenalty(lines):
	for line in lines:
		if 'class="GP"' in line:
			return true
	return false


def processLeague():
	#infile = open('liga2014-15.html', 'r')
	#for line in infile:

	urlLeague = 'http://www.bdfutbol.com/es/t/t2014-15.html'
	league = urllib2.urlopen(urlLeague)

	for line in league:
		if "/p/p.php?id=" in line:
			extractLinksFromLine(line)

def processLeagueWhoScored():
	urlBase = 'http://www.whoscored.com/Matches/'
	#http://www.whoscored.com/Matches/862052/Live
	start = 862052
	end = 870000
	cont = start
	while ( cont <= end):
		url = urlBase + str(cont) + "/Live"
		print url
		#processURL(url)
		theTitle = getPage(url)
		#theTitle = extractTitle(thePageHTML)
		print theTitle
		cont +=1




#Open file
#f = open('output_t2014-15.txt', 'w')
processLeagueWhoScored()
#f.close()
