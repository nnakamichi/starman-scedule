# -*- Coding: utf-8 -*-
from bs4 import BeautifulSoup as bs
import requests
from datetime import datetime
import csv
import json
import urllib.parse
import boto3

print('Loading function')

s3 = boto3.client('s3')

def lambda_handler(event, context):
    try:
        dt_now = datetime.now()
        ym = str(dt_now.year) + str(dt_now.month)
        html = requests.get('https://www.baystars.co.jp/community/mascot/schedule/{0}.php'.format(ym)).text
        soup = bs(html, "html.parser")
        tds = soup.find('table', attrs={"class":"schedule_calendar"}).find_all("td", attrs={"style": "height:79px!important;"})

        work_days = []
        for td in tds:
            a = td.find("a")
            if a:
                day = a.find("p").text
                starman_flg = a.ul.li.find("img", attrs={"alt": "DB.スターマン"})
                if starman_flg:
                    work_days.append(day)

        with open('/tmp/work_days.csv', 'w') as wf:
            writer = csv.writer(wf, lineterminator='\n')
            writer.writerow(work_days)
    except Exception as e:
        print(e)
        raise e
