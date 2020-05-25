from selenium import webdriver  # Import module
import time  # Waiting function


def get_data_link():

    home_page_url = "https://public.tableau.com/views/RapidCOVID-19virology-Public/Headlinesummary?:display_count=y&:embed=y&:showAppBanner=false&:showVizHome=no"  # Define URL
    xpath = '//*[@id="tabZoneId66"]/div/div/div/a'

    browser = webdriver.Safari()
    browser.get(home_page_url)
    time.sleep(2)
    # browser.maximize_window()

    element = browser.find_element_by_id("tabZoneId66")
    result = element.find_element_by_xpath(xpath)
    url = result.get_attribute("href")

    return url
