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

spans = driver.find_elements_by_class_name('page-navigation-item')
for span in spans:
	print span

print "adios"