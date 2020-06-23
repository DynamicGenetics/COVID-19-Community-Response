import schedule
import time
import functools
import logging

# NB Necessary to set up the logging config before importing the variables from other scripts
logging.basicConfig(
    filename="scheduler.log",
    filemode="a",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# --------------
# Local imports
# --------------
from generate_json import DATA

from datasets import LIVE_DATA_FOLDER, LIVE_RAW_DATA_FOLDER, GEO_DATA_FOLDER
from scrapers.police_coders_groups.run_scraper import run_police_coders_scraper
from scrapers.phw_covid_statement.phw_scraper import run_phw_scraper

# ---------------------
# Logging wrap function
# ---------------------

# Set up logging object, logger
logger = logging.getLogger(__name__)


# Note: logging wrapper taken from docs https://schedule.readthedocs.io/en/stable/faq.html
def with_logging(func):
    """This is a wrapper that logs the start and end of a function."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger.info('Running job "%s"' % func.__name__)
        result = func(*args, **kwargs)
        logger.info('Job "%s" completed' % func.__name__)
        return result

    return wrapper


# ----------------
# Functions to run
# ----------------


@with_logging
def run_scrapers():
    # Get latest covid case data from PHW
    run_phw_scraper(LIVE_RAW_DATA_FOLDER, LIVE_DATA_FOLDER)
    # run  Coders community group scra
    run_police_coders_scraper(LIVE_RAW_DATA_FOLDER, LIVE_DATA_FOLDER, GEO_DATA_FOLDER)


@with_logging
def update_json():
    DATA.write()


if __name__ == "__main__":

    run_scrapers()
    update_json()

    # # Run scrapers at 3pm UTC, which is 4pm UTC
    # schedule.every().day.at("15:00").do(job)

    # # Generate new JSON after running the scrapers
    # schedule.every().day.at("")

    # # Sleep function
    # while True:
    #     schedule.run_pending()
    #     time.sleep(42)
