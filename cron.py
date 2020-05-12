from crontab import CronTab

def main():

    cron = CronTab()
    job = cron.new('python main.py')
    job.setall('00 00 * * *')
    for result in cron.run_scheduler():
        print("Done")
 
if __name__ == "__main__":
    main()

