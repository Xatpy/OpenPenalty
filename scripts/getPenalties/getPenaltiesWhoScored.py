from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import time

SPANISH_TEAMS = ["Atletico Madrid", "Real Madrid", "Barcelona", "Valencia", "Sevilla",
				 "Villareal", "Athletic Bilbao", "Celta Vigo", "Malaga", "Espanyol", "Rayo Vallecano", "Real Sociedad",
				 "Elche", "Levante", "Getafe", "Deportivo La Coruna", "Granada", "Eibar", "Almeria", "Cordoba",
				 "Real Betis"]

def out(message, file):
	file.write(message.encode('utf8') + '\n')
	print message


def getTeams(title, f):
	teams = title.split("-")
	spanish_match = True
	for tm in teams:
		if tm not in SPANISH_TEAMS:
			#print tm + " not Spanish.---"
			message = tm + " not Spanish.---"
			out (message, f)
			return False;
	return spanish_match

def checkPenalty(list, type, f):
	contador = 0
	for el in list:
		contador += 1
		if el.text:
			eventText = el.text.replace('\n',' ')
			#eventText = el.text.upper()
			if "PENALTY" in eventText.upper():
				#print "\t" + type + " - " + eventText
				message = "\t" + type + " - " + eventText
				out(message,f)
		#print str(contador) + " - " + el.text

### ----- Driver setup ------
driver = webdriver.Firefox()
driver.maximize_window()
#driver.set_window_position(-110,-600)
driver.maximize_window()
driver.delete_all_cookies()

with open('outFile.txt', 'w+') as f:

	message = ":::OpenPenalty: Start script at::: " + time.ctime()
	out (message, f)

	baseURL = "http://www.whoscored.com/Matches/"


	#urlList = ["http://www.whoscored.com/Matches/985501/Live", "http://www.whoscored.com/Matches/985519/Live", "http://www.whoscored.com/Matches/985563/Live",
	#		   "http://www.whoscored.com/Matches/985555/Live", "http://www.whoscored.com/Matches/985553/Live"]
	urlList = []
	#url = "http://www.whoscored.com/Matches/985501/Live"

	#build url list
	i = 862052
	fin = 862258
	while i < fin:
		i += 1
		url_aux = baseURL + str(i) + "/Live"
		urlList.append(url_aux)

	for url in urlList:
		driver.get(url)
		#print "que pasa" + url

		spanishMatch = getTeams(driver.title, f)

		message = "# Match: " + driver.title + " | URL: " + url
		out (message, f)

		if spanishMatch:
			links = driver.find_elements_by_partial_link_text('Match Commentary')
			for link in links:
				#print link.get_attribute("href")
				link.click()

			#print "aqui estamos"
			total_pages_text = driver.find_element_by_class_name('total-pages')

			totalPages = int(total_pages_text.text)
			currentPage = 0
			while currentPage < totalPages:
				currentPage += 1
				list15 = driver.find_elements_by_xpath("//*[@data-type=15]")
				checkPenalty(list15, "FAIL", f)
				list16 = driver.find_elements_by_xpath("//*[@data-type=16]")
				checkPenalty(list16, "GOAL", f)

				#print "Next page"
				spans = driver.find_elements_by_class_name('page-navigation-item')
				spans[2].click()

print "end script"