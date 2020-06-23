from selenium import webdriver  # Import module
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import time  # Waiting function
from warnings import warn
import os
import logging


def get_data_link():
    """Use Selenium to open a Chrome window and get the url link of most recent dataset"""
    home_page_url = "https://public.tableau.com/views/RapidCOVID-19virology-Public/Headlinesummary?:display_count=y&:embed=y&:showAppBanner=false&:showVizHome=no"  # Define URL

    # Set chrome to be headless (i.e. doesn't open the webpage GUI)
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    # Set browser to be headerless Chrome
    browser = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    browser.get(home_page_url)  # Go to the homepage url
    time.sleep(5)  # Wait for it to load

    def get_url():
        element = browser.find_element_by_id("tabZoneId66")
        xpath = '//*[@id="tabZoneId67"]/div/div/div/div[1]/div/span/div[3]/span/a'
        result = element.find_element_by_xpath(xpath)
        return result.get_attribute("href")

    try:
        url = get_url()
    except NoSuchElementException:
        logging.warn("Element not found")
        time.sleep(10)
        url = get_url()
    finally:
        browser.quit()

    return url
