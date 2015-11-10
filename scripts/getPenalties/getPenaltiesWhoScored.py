from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import time

SPANISH_TEAMS = ["Atletico Madrid", "Real Madrid", "Barcelona", "Valencia", "Sevilla", "Real Betis",
				 "Villareal", "Villarreal", "Athletic Club", "Athletic Bilbao", "Celta Vigo", "Malaga", "Espanyol", "Rayo Vallecano", "Real Sociedad",
				 "Elche", "Levante", "Getafe", "Deportivo La Coruna", "Granada", "Eibar", "Almeria", "Cordoba"]

ENGLISH_TEAMS = ["Arsenal", "Sunderland", "West Bromwich Albion", "Aston Villa", "Burnley", "Chelsea", "Sunderland", "crystal Palace", "Swansea", "Everton",
				 "Tottenham", "Hull", "Manchester United", "Leicester", "Queens Park Rangers", "Manchester City", "Southampton", "Newcastle United", "West Ham", "Stoke", "Liverpool"]

GERMAN_TEAMS = ["Bayern Munich", "Mainz 05", "Borussia Dortmund", "Werder Bremen", "Borussia M.Gladbach", "Augsburg","Hoffenheim","Hertha Berlin","Hannover 96","Freiburg","Eintracht Frankfurt",
				"Bayer Leverkusen","Hamburger SV","Schalke 04","FC Cologne","Wolfsburg","Paderborn","VfB Stuttgart"]

ITALIAN_TEAMS = ["Lazio","Roma","Verona","Juventus","Atalanta","AC Milan","Cagliari","Udinese","Torino","Cesena","Fiorentina","Chievo","Inter",
				 "Empoli","Sassuolo","Genoa","Napoli","Lazio","Roma","Palermo","Sampdoria","Parma"]

def out(message, file):
	file.write(message.encode('utf8') + '\n')
	print message

# Returns: -1 == No coincidence
# 			0 == Spanish
#          	1 == English
#			2 == German
#			3 == Italian
def getNationalities(title, f, url):
	teams = title.split("-")
	if len(teams) != 2:
		message = "NO CORRECT MATCH " + title + +'\t' + url + " not found.---"
		out (message, f)
		return -1

	if teams[0] in SPANISH_TEAMS and teams[1] in SPANISH_TEAMS:
		return 0 	# Spanish
	elif teams[0] in ENGLISH_TEAMS and teams[1] in ENGLISH_TEAMS:
		return 1 	# English
	elif teams[0] in GERMAN_TEAMS and teams[1] in GERMAN_TEAMS:
		return 2 	# German
	elif teams[0] in ITALIAN_TEAMS and teams[1] in ITALIAN_TEAMS:
		return 3 	# Italian

	# Other teams
	message = title + " not found.---"
	out (message, f)
	return -1			# Not found

def checkPenalty(list, type, f, messageMatch):
	contador = 0
	for el in list:
		contador += 1
		if el.text:
			eventText = el.text.replace('\n',' ')
			if "PENALTY" in eventText.upper():
				message = '\t' + type + " - " + eventText + '\t' + messageMatch
				out(message, f)

def buildUrlList(urlList, i, fin):
	if i > fin:
		print "Error loop buildUrlList"
		return
	while i < fin:
		i += 1
		url_aux = baseURL + str(i) + "/Live"
		urlList.append(url_aux)

### ----- Driver setup ------
driver = webdriver.Firefox()
driver.maximize_window()
driver.maximize_window()
driver.delete_all_cookies()

extraDebug = True

with open('outScript.txt', 'w+') as fScr, open('outSpanish.txt', 'w+') as fSpanish, open('outEnglish.txt', 'w+') as fEnglish, \
	 open('outGerman.txt', 'w+') as fGerman, open('outItalian.txt', 'w+') as fItalian:

	message = ":::OpenPenalty: Start script at::: " + time.ctime()
	out (message, fScr)

	baseURL = "http://www.whoscored.com/Matches/"

	urlList = []

	#Build URL list
		# Spanish 14-15
		# buildUrlList(urlList, 862052, 862258)
	# English 14-15
	buildUrlList(urlList, 829513, 829848)
	# German 14-15
	buildUrlList(urlList, 834589, 834899)
	# Italian 14-15
	buildUrlList(urlList, 865781, 866178)

	#urlList = ['http://www.whoscored.com/Matches/829799/Live', 'http://www.whoscored.com/Matches/862058/Live']

	for url in urlList:
		time.sleep(31)
		driver.get(url)

		typeNat = getNationalities(driver.title, fScr, url)

		fileAux = None
		if (typeNat == -1):
			continue
		elif (typeNat == 0):
			fileAux = fSpanish
		elif (typeNat == 1):
			fileAux = fEnglish
		elif typeNat == 2:
			fileAux = fGerman
		elif typeNat == 3:
			fileAux = fItalian

		messageMatch = "# Match: " + driver.title + " | URL: " + url
		#if extraDebug:
			#out (messageMatch, fScr)

		if typeNat > 0:
			links = driver.find_elements_by_partial_link_text('Match Commentary')
			for link in links:
				link.click()

			total_pages_text = driver.find_element_by_class_name('total-pages')

			totalPages = int(total_pages_text.text)
			currentPage = 0
			while currentPage < totalPages:
				currentPage += 1
				list15 = driver.find_elements_by_xpath("//*[@data-type=15]")
				checkPenalty(list15, "FAIL", fileAux, messageMatch)
				list16 = driver.find_elements_by_xpath("//*[@data-type=16]")
				checkPenalty(list16, "GOAL", fileAux, messageMatch)

				#print "Next page"
				spans = driver.find_elements_by_class_name('page-navigation-item')
				spans[2].click()

print "end script"
