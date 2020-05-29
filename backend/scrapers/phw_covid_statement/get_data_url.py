from selenium import webdriver  # Import module
from selenium.common.exceptions import NoSuchElementException
import time  # Waiting function
from warnings import warn


def get_data_link():
    """Use Selenium to open a Safari window and get the url link of most recent dataset"""
    home_page_url = "https://public.tableau.com/views/RapidCOVID-19virology-Public/Headlinesummary?:display_count=y&:embed=y&:showAppBanner=false&:showVizHome=no"  # Define URL

    browser = webdriver.Safari()  # Open Safari
    browser.get(home_page_url)  # Go to the homepage url
    time.sleep(5)  # Wait for it to load

    def get_url():
        element = browser.find_element_by_id("tabZoneId66")
        xpath = '//*[@id="tabZoneId66"]/div/div/div/a'
        result = element.find_element_by_xpath(xpath)
        return result.get_attribute("href")

    try:
        url = get_url()
    except NoSuchElementException:
        warn(
            "Can't find the element. I'm going to wait 10 seconds \n"
            "in case the webpage still needs to load."
        )
        time.sleep(10)
        url = get_url()
    finally:
        browser.quit()

    return url
