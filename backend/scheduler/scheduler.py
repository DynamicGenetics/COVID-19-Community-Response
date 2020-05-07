import schedule

# Some schedule scripts for dynamic genetics groups projects

def schedule(run_frequency_in_days):

    """ Schedule sets up a time to execute other tasks.
    When waiting to run, your python script will be in an Sl state:
    interuptable sleeping state.

    Syntax for schedule:
    schedule.every(10).minutes.do(job)
    schedule.every().hour.do(job)
    schedule.every().day.at("10:30").do(job)
    schedule.every(5).to(10).minutes.do(job)
    schedule.every().monday.do(job)
    schedule.every().wednesday.at("13:15").do(job)
    schedule.every().minute.at(":17").do(job)"""

    # run task at 6amUTC (night for most of Europe and US: less rate limiting)
    schedule.every(run_frequency_in_days).days.at("06:00").do(main)


def main_scheduler(run_frequency_in_days):

    if __name__ == '__main__':
        main() # run the process immediately on calling the script.
        schedule(run_frequency_in_days) # repeat time

        while True:
            schedule.run_pending()
            time.sleep(42) # wait a few seconds in case anything needs to finish up


def mongoexport_scheduler(run_frequency_in_days):

    schedule(run_frequency_in_days) # repeat time

    while True:
        schedule.run_pending()
            time.sleep(42) # wait a few seconds in case anything needs to finish up
