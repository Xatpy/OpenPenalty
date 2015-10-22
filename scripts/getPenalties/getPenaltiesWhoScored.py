from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

driver = webdriver.Firefox()

driver.maximize_window()
#driver.set_window_position(-110,-600)
driver.maximize_window()

driver.delete_all_cookies()

print "ey"

driver.get('http://www.whoscored.com/Matches/985501/Live')

print "que pasa"

links = driver.find_elements_by_partial_link_text('Match Commentary')
for link in links:
    print link.get_attribute("href")
    link.click()

#element = WebDriverWait(driver, 500).until(
#    EC.presence_of_element_located((By.CLASS_NAME,'wizards_mod'))
#)
#debugger('Click on wizards')
#element.click()

print "aqui estamos"
total_pages = driver.find_element_by_class_name('total-pages')
print total_pages.text

#spans = driver.find_elements_by_class_name('page-navigation-item')
#for span in spans:
	#print span
	
test = driver.find_element_by_xpath("//*[@data-type=16]")
if (test):
	print "si"
else:
	print "no"

if 0:
	elementA = WebDriverWait(driver, 5).until(
		#EC.presence_of_element_located((By.CLASS_NAME, "//*[@data-type=16]"))
		EC.presence_of_element_located((By.XPATH, "//*[@data-type=1500]"))
		#elementA = driver.find_elements_by_xpath("//*[@data-type=16]")
	)
	if (elementA):
		print "siiiii"
	else:
		print "nooooo"
	#debugger('Click on wizards')
	#elementA.click()

list15 = driver.find_elements_by_xpath("//*[@data-type=15]")
contador = 0
for el in list15:
	contador += 1
	print str(contador) + " - " + el.text
list16 = driver.find_elements_by_xpath("//*[@data-type=16]")
list1500 = driver.find_elements_by_xpath("//*[@data-type=1500]")



print "adios"