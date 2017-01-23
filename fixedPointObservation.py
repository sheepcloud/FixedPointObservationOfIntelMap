#!/usr/bin/env python

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from xvfbwrapper import Xvfb
from datetime import datetime
import os
import time
import lxml.html
from selenium.webdriver.support import expected_conditions as EC
import sys
import settings

class CapturePages(object):

    def __init__(self):
        print ("f:__init__")
        self.xvfb = Xvfb(1280, 1280)
        self.xvfb.start()

        fp = webdriver.FirefoxProfile()
        fp.set_preference('intl.accept_languages', 'ja-JP, ja')
        self.browser = webdriver.Firefox(firefox_profile=fp)
        self.browser.set_window_size(self.xvfb.width, self.xvfb.height)


    def myfunc(self, x):
        print ("f:myfunc")
        root = lxml.html.fromstring(self.browser.page_source)
        print (root)
        loading_div = root.xpath("//*[@id='loading_msg']")
        dispAttrib = loading_div[0].attrib.get("display")
        print (loading_div[0])
        print (dispAttrib is None)
        if dispAttrib is None:
            print ("wait 2sec")
            time.sleep(2)
            return False
        
        print ("load finish")
        return True


    def waitLoadPage(self):
        print ("f:waitLoadPage")
        try:
            start = time.time()
            wait = WebDriverWait(self.browser, 120)
            element = wait.until(EC.invisibility_of_element_located((By.XPATH, '//*[@id="loading_msg"]')))
            elapsed_time = time.time() - start 
            print ("d:" + str(elapsed_time))
        except TimeoutException:
            print ("Timeout!")


    def login(self):
        print ("f:login")
        self.browser.get("https://www.google.com/accounts/ServiceLogin?service=ah&passive=true&continue=https://appengine.google.com/_ah/conflogin%3Fcontinue%3Dhttps://www.ingress.com/intel&ltmpl=gm&shdf=ChMLEgZhaG5hbWUaB0luZ3Jlc3MMEgJhaCIUDxXHTvPWkR39qgc9Ntp6RlMnsagoATIUG3HUffbxSU31LjICBdNoinuaikg")
        time.sleep(5)

        email = self.browser.find_element_by_name("Email")
        email.send_keys(settings.email)
        email.send_keys(Keys.RETURN)
        print ("d:Email")
        time.sleep(5)

        passwd = self.browser.find_element_by_name("Passwd")
        passwd.send_keys(settings.password)
        passwd.send_keys(Keys.RETURN)
        print ("d:Passwd")
        time.sleep(5)


    def viewIntelMap(self):
        print ("f:viewIntelMap")
        self.browser.get(settings.captureUrl)
        time.sleep(10)
        self.waitLoadPage();


    def setDisplay(self):
        print ("f:setDisplay")
        self.browser.execute_script("document.getElementById('header').style.display = 'none';")
        self.browser.execute_script("document.getElementById('tm_button').style.display = 'none';")
        self.browser.execute_script("document.getElementById('player_stats').style.display = 'none';")
        self.browser.execute_script("document.getElementById('game_stats').style.display = 'none';")
        self.browser.execute_script("document.getElementById('geotools').style.display = 'none';")
        self.browser.execute_script("document.getElementById('comm').style.display = 'none';")
        self.browser.execute_script("document.getElementById('comm').style.display = 'none';")
        self.browser.execute_script("document.getElementById('filters_container').style.display = 'none';")
        self.browser.execute_script("document.getElementById('portal_filter_header').style.display = 'none';")

        elem = self.browser.find_element_by_xpath('//*[@id="map_canvas"]/div/div[8]')
        self.browser.execute_script("arguments[0].style.display = 'none';", elem) 

        elem = self.browser.find_element_by_xpath('//*[@id="map_canvas"]/div/div[10]')
        self.browser.execute_script("arguments[0].style.display = 'none';", elem) 

        elem = self.browser.find_element_by_xpath('//*[@id="map_canvas"]/div/div[12]')
        self.browser.execute_script("arguments[0].style.display = 'none';", elem) 


    def capturePage(self):
        print ("f:capturePage")
        self.browser.save_screenshot("test.png")
        check = os.system('./run.sh')


    def dispose(self):
        print ("f:dispose")
        self.browser.close()
        self.xvfb.stop()


if __name__ == '__main__':

    debugMode = "debug" in sys.argv    

    if debugMode:
        print ("debug mode")

    capPages = CapturePages();
    try:
        capPages.login()
        while True:
            if debugMode or (datetime.now().minute % 10 == 0):
                capPages.viewIntelMap()
                capPages.setDisplay()
                capPages.capturePage()
            if debugMode:
                break
            time.sleep(60)
    except :
        print (sys.exc_info()[0])
    capPages.dispose()

