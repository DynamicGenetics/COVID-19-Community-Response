import schedule
import time
import functools
import logging

from generate_json import DATA

from datasets import LIVE_DATA_FOLDER, LIVE_RAW_DATA_FOLDER, GEO_DATA_FOLDER
from scrapers.police_coders_groups.run_scraper import run_police_coders_scraper
from scrapers.phw_covid_statement.phw_scraper import run_phw_scraper

# --------------
# Set up logging
# --------------

logger = logging.getLogger(__name__)


def with_logging(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print('LOG: Running job "%s"' % func.__name__)
        result = func(*args, **kwargs)
        print('LOG: Job "%s" completed' % func.__name__)
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
def rewrite_json():
    DATA.write()


if __name__ == "__main__":

    run_scrapers()
    DATA.write()

    # # Run scrapers at 3pm UTC, which is 4pm UTC
    # schedule.every().day.at("15:00").do(job)

    # # Generate new JSON after running the scrapers
    # schedule.every().day.at("")

    # # Sleep function
    # while True:
    #     schedule.run_pending()
    #     time.sleep(42)
