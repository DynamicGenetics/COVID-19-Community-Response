"""This module is responsible for the automated updating of the COVID cumulative
cases data from Public Health Wales, and fetching groups from Police Coders.
When run as main it will execute both scrapers daily at 3pm, and update the JSON 5
minutes later at 3.05pm. If a task raises an exception, it will
send a notification to the lab Slack group to notify us to check the logs."""

import time
import functools
import traceback
import logging
import datetime
import sys
from traceback import format_exc
from slack import WebClient
from schedule import Scheduler

from slack_tokens import SLACK_TOKEN, SLACK_CHANNEL
from datasets import LIVE_DATA_FOLDER, LIVE_RAW_DATA_FOLDER, GEO_DATA_FOLDER
from scrapers.police_coders_groups.run_scraper import run_police_coders_scraper
from scrapers.phw_covid_statement.phw_scraper import run_phw_scraper

# NB Necessary to set up the logging config before running the local imports
logging.basicConfig(
    filename="scheduler.log",
    filemode="a",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# ------
# Set up
# ------
# Initialise logger
logger = logging.getLogger("scheduler")
# Slack connection set up
client = WebClient(token=SLACK_TOKEN)


# Source https://gist.github.com/mplewis/8483f1c24f2d6259aef6
class SafeScheduler(Scheduler):
    """
    An implementation of Scheduler that catches jobs that fail, logs their
    exception tracebacks as errors, optionally reschedules the jobs for their
    next run time, and keeps going.

    Use this to run jobs that may or may not crash without worrying about
    whether other jobs will run or if they'll crash the entire script.
    """

    def __init__(self, reschedule_on_failure=True):
        """
        If reschedule_on_failure is True, jobs will be rescheduled for their
        next run as if they had completed successfully. If False, they'll run
        on the next run_pending() tick.
        """
        self.reschedule_on_failure = reschedule_on_failure
        super().__init__()

    def _run_job(self, job):
        try:
            super()._run_job(job)
        except Exception:
            logger.error(format_exc())
            job.last_run = datetime.datetime.now()
            job._schedule_next_run()


# ---------------------
# Logging wrap function
# ---------------------
# Note: logging wrapper taken from docs https://schedule.readthedocs.io/en/stable/faq.html
def with_logging(func):
    """This is a wrapper that logs the start and end of a function,
    and sends exceptions to Slack"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger.info('Running job "%s"' % func.__name__)
        try:
            result = func(*args, **kwargs)
        except Exception as e:

            message = (
                "Hello from ErrorBot! :tada: An exception "
                "has been raised by the scheduling system, inside SafeScheduler."
                "Here is the traceback: {}".format(traceback.print_exc())
            )

            client.chat_postMessage(
                channel=SLACK_CHANNEL, text=message,
            )
            raise e
        logger.info('Job "%s" completed' % func.__name__)

        return result

    return wrapper


# ----------------
# Functions to run
# ----------------
@with_logging
def run_scrapers():
    run_phw_scraper(LIVE_RAW_DATA_FOLDER, LIVE_DATA_FOLDER)
    run_police_coders_scraper(LIVE_RAW_DATA_FOLDER, LIVE_DATA_FOLDER, GEO_DATA_FOLDER)


@with_logging
def update_json():
    # Re-run the import each time to ensure the imported DATA object is not saved in memory
    from generate_json import DATA

    DATA.write()


if __name__ == "__main__":

    try:
        client.chat_postMessage(
            channel=SLACK_CHANNEL,
            text="Thanks, the scheduler is up and running again. :raised_hands:",
        )

        # Run safe scheduler every day at 4pm and 4.15pm BST
        scheduler = SafeScheduler()

        scheduler.every().day.at("15:00").do(run_scrapers)
        scheduler.every().day.at("15:05").do(update_json)

        # Sleep function
        while True:
            scheduler.run_pending()
            time.sleep(60)

    except Exception as e:
        message = (
            ":skull: It's a me, ErrorBot! Unfortunately the scheduler script has stopped running.\n"
            "{}".format(traceback.format_exc())
        )

        client.chat_postMessage(channel=SLACK_CHANNEL, text=message)

        logger.critical(
            "Running script terminated. Message sent to Slack. Traceback was {}".format(
                traceback.format_exc()
            )
        )

        raise e
