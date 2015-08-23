import urllib2

BASE_URL = "http://www.bdfutbol.com/es"

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
	infile = open('liga2014-15.html', 'r')

	for line in infile:
		if "/p/p.php?id=" in line:
			extractLinksFromLine(line)


#Open file
f = open('output.txt', 'w')
processLeague()
f.close()
