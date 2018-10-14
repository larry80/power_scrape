from apscheduler.schedulers.blocking import BlockingScheduler
from bge import main, BaseBgeScraper
from bs4 import BeautifulSoup as bs
import requests
import xml.etree.ElementTree as et
import time
import json
import datetime
import mysql.connector
import myconfig
import logging

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=1)
def print_data():
    print('starting job')
    main()

#@sched.scheduled_job('cron', day_of_week='sat-sun', hour='8-14', minute='0-59/10', timezone='America/New_York')
#def update_a():
# 	your_function_a()

#@sched.scheduled_job('cron', day_of_week='fri', hour='15-19/2', timezone='America/New_York')
#def update_b():
# 	your_function_b()

#sched.start()
#sched.shutdown()
sched.shutdown()
