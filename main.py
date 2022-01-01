from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time

channel_url = 'https://www.youtube.com/channel/UC_0IIMmTZvnfO9ucN87qUhQ/videos'

while True:
    options = webdriver.ChromeOptions()
    options.binary_location = os.environ.get('GOOGLE_CHROME_BIN')
    options.add_argument("--incognito")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--headless")
    browser = webdriver.Chrome(executable_path=os.environ.get('CHROMEDRIVER_PATH'),options=options)
    # browser = webdriver.Chrome(executable_path='C:/Program Files (x86)/Chrome Driver/chromedriver.exe')
    browser.get(channel_url)

    # get list of youtube videos titles
    vids_list = browser.find_elements_by_css_selector('a[class*=yt-simple-endpoint ]')
    # get list of links for all videos
    links = [elem.get_attribute('href') for elem in vids_list]

    for link in links:
        if link and 'watch' in link:
            browser.execute_script("window.open('');")
            browser.switch_to.window(browser.window_handles[-1])
            browser.get(link)
            # wait until button is loaded on screen
            elem = WebDriverWait(browser, 20).until(EC.element_to_be_clickable(
            (By.CLASS_NAME, "ytp-play-button")))
            # click only if button is of label 'play' not 'pause'.
            if elem.get_attribute('aria-label') == 'Play (k)':
                print('Currently watching:', link)
                elem.click()
            time.sleep(30)

    time.sleep(3000)
    browser.quit()