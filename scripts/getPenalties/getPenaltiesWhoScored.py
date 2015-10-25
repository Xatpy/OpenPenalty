from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

SPANISH_TEAMS = ["Atletico Madrid", "Real Madrid"]

def getTeams(title):
	teams = title.split("-")
	spanish_match = True
	for tm in teams:
		print tm
		if tm not in SPANISH_TEAMS:
			return False;
	return spanish_match

def checkPenalty(list, type):
	contador = 0
	for el in list:
		contador += 1
		eventText = el.text.upper()
		if el.text:
			if "PENALTY" in eventText:
				print type + " - " + el.text
		#print str(contador) + " - " + el.text

driver = webdriver.Firefox()
driver.maximize_window()
#driver.set_window_position(-110,-600)
driver.maximize_window()
driver.delete_all_cookies()

print "start"

urlList = ["http://www.whoscored.com/Matches/985501/Live", "http://www.whoscored.com/Matches/985519/Live", "http://www.whoscored.com/Matches/985563/Live"]

#url = "http://www.whoscored.com/Matches/985501/Live"
#url = "http://www.whoscored.com/Matches/985519/Live"

for url in urlList:
	driver.get(url)

	print "que pasa" + url

	getTeams(driver.title)

	links = driver.find_elements_by_partial_link_text('Match Commentary')
	for link in links:
		print link.get_attribute("href")
		link.click()

	print "aqui estamos"
	total_pages_text = driver.find_element_by_class_name('total-pages')

	totalPages = int(total_pages_text.text)
	currentPage = 0
	while currentPage < totalPages:
		currentPage += 1
		list15 = driver.find_elements_by_xpath("//*[@data-type=15]")
		checkPenalty(list15, "FALLO")
		list16 = driver.find_elements_by_xpath("//*[@data-type=16]")
		checkPenalty(list16, "GOL")

		print "vamos a por el siguiente"
		spans = driver.find_elements_by_class_name('page-navigation-item')
		spans[2].click()

print "adios"