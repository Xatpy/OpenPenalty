from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import time

SPANISH_TEAMS = ["Atletico Madrid", "Real Madrid", "Barcelona", "Valencia", "Sevilla",
				 "Villareal", "Athletic Club", "Celta Vigo", "Malaga", "Espanyol", "Rayo Vallecano", "Real Sociedad",
				 "Elche", "Levante", "Getafe", "Deportivo La Coruna", "Granada", "Eibar", "Almeria", "Cordoba",
				 "Real Betis"]

def getTeams(title):
	teams = title.split("-")
	spanish_match = True
	for tm in teams:
		if tm not in SPANISH_TEAMS:
			print tm + " not Spanish.---"
			return False;
	return spanish_match

def checkPenalty(list, type):
	contador = 0
	for el in list:
		contador += 1
		if el.text:
			eventText = el.text.replace('\n',' ')
			#eventText = el.text.upper()
			if "PENALTY" in eventText.upper():
				print "\t" + type + " - " + eventText
		#print str(contador) + " - " + el.text

driver = webdriver.Firefox()
driver.maximize_window()
#driver.set_window_position(-110,-600)
driver.maximize_window()
driver.delete_all_cookies()

print ":::OpenPenalty: Start script at::: " + time.ctime()


baseURL = "http://www.whoscored.com/Matches/"


urlList = ["http://www.whoscored.com/Matches/985501/Live", "http://www.whoscored.com/Matches/985519/Live", "http://www.whoscored.com/Matches/985563/Live",
		   "http://www.whoscored.com/Matches/985555/Live", "http://www.whoscored.com/Matches/985553/Live"]

#url = "http://www.whoscored.com/Matches/985501/Live"

for url in urlList:
	driver.get(url)
	#print "que pasa" + url

	spanishMatch = getTeams(driver.title)

	print "# Match: " + driver.title + " | URL: " + url

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
			checkPenalty(list15, "FAIL")
			list16 = driver.find_elements_by_xpath("//*[@data-type=16]")
			checkPenalty(list16, "GOAL")

			#print "Next page"
			spans = driver.find_elements_by_class_name('page-navigation-item')
			spans[2].click()

print "end script"