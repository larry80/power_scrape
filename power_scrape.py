from bs4 import BeautifulSoup as bs
import requests
import xml.etree.ElementTree as et
import time
import json
import datetime
import mysql.connector
import myconfig
from apscheduler.schedulers.blocking import BlockingScheduler



cnx = mysql.connector.connect(user=myconfig.power_user, password=myconfig.power_pass, host='192.168.1.10', database=myconfig.power_db)
cursor = cnx.cursor()
db_timestamp = datetime.datetime.utcnow()
ts = db_timestamp.strftime('%Y-%m-%d %H:%M:%S')




"""
https://s3.amazonaws.com/outagemap.bge.com/data/interval_generation_data/metadata.xml
https://s3.amazonaws.com/outagemap.bge.com/data/interval_generation_data/2018_10_13_01_18_27/report.js?timestamp=1539407984881
https://s3.amazonaws.com/outagemap.bge.com/data/interval_generation_data/2018_10_13_01_25_29/data.js?timestamp=1539408335443
"""

def main():
    print('starting')
    BaseBgeScraper()

def BaseBgeScraper():
    metadata_url = 'https://s3.amazonaws.com/outagemap.bge.com/data/interval_generation_data/metadata.xml'
    metadata = requests.get(metadata_url)
    metadata_content = bs(metadata.content, 'html.parser') 
    directory = metadata_content.find_all('directory')[0].text
    data_url = 'https://s3.amazonaws.com/outagemap.bge.com/data/interval_generation_data/%s/report.js?timestamp=%d' % (directory, int(time.time()))
    current_outages = requests.get(data_url)
    to_insert = []
    if current_outages.status_code == 200:
        outage_data = json.loads(current_outages.content.decode('utf-8'))
    else:
        pass
    if outage_data is not None:
        for row in outage_data['file_data']['curr_custs_aff']['areas']:
            for county in row['areas']:
                tmp_insert = ts, str('BGE'), str(county['area_name']).replace('\'', ''), county['custs_out'], county['custs_rest'], county['total_custs']
                to_insert.append(tmp_insert)
        sql_stmt = 'INSERT INTO thor.bge (insert_ts, utility, area_name, custs_out, custs_rest, total_custs) VALUES (%s, %s, %s, %s, %s, %s)'
        cursor.executemany(sql_stmt, to_insert)
        cnx.commit()
        cursor.close()
    else:
        print('fail')

#sched = BlockingScheduler()
#sched.add_job(main, 'cron', minute='4')

#sched.start()

main()