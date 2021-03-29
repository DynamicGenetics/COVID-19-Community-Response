import requests
from bs4 import BeautifulSoup
from warnings import warn
import os
import logging

logger = logging.getLogger(__name__)


def get_data_link():
    """Get the link of the latest COVID dataset.
    """

    # Get the content from the webpage
    response = requests.get(
        "http://www2.nphs.wales.nhs.uk:8080/CommunitySurveillanceDocs.nsf/PublicPage?OpenPage&AutoFramed"
    )
    # Parse the content using Beautiful Soup
    soup = BeautifulSoup(response.content, "html.parser")
    # Find the element with the title that we need, and get the parent row (<tr>)
    element = soup.find(title="Rapid COVID-19 surveillance data").find_parent("tr")
    # Extract the URL from the row element (it is the first href in the row.)
    url = "http://www2.nphs.wales.nhs.uk:8080" + element.find("a").get("href")

    return url
