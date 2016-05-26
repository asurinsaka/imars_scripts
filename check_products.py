#!/usr/bin/env python
# coding=utf-8

from datetime import datetime , timedelta
from pytz import timezone
import pytz
import requests
from bs4 import BeautifulSoup

# This function check whether the number of links are equal or more than
#   expected number
def product_count(sat, type, products):
    count = 0
    for product in products:
        if sat in product and type in product:
            count += 1
    return count

# check the number of products of a date
def check_products(date, mod_sst, mod_chlor, viirs_sst, viirs_chlor):
    url = 'http://imars.marine.usf.edu/legacy-names/index.php?area=a05&date='+ str(date)
    page = requests.get(url).text
    soup = BeautifulSoup(page, 'html.parser')
    products =  [ node.get('href').encode('UTF8') for node in
                 soup.find_all('a') if 'tiff' in
                 node.get('href').encode('UTF8')]
    report = ''
    report += "mod_sst " if mod_sst > product_count("modis",'sst',products) else ''
    report += "mod_chlor " if mod_chlor > product_count("modis",'chl',products) else ''
    report += "viirs_sst " if viirs_sst > product_count("viirs",'sst',products) else ''
    report += "viirs_chlor " if viirs_chlor> product_count("viirs",'chl',products) else ''
    return report


# get the current date and time in utc (system timezone)
now =datetime.now()
utc = pytz.utc
eastern = timezone('US/Eastern')
utc_time = utc.localize(now)

# convert to tampa time
edt_time = utc_time.astimezone(eastern)
# check today's products after 10 am
today10am = edt_time.replace(hour=10,minute=0,second=0,microsecond=0)
yesterday = datetime.now() - timedelta(days=1)

# always check total number of yesterday's products
error_products = check_products(yesterday.date(), 7,3,4,2)
if edt_time > today10am:
    error_products += check_products(datetime.now().date(), 4, 0, 2, 0)

if error_products == '':
    print "OK: All Good!"
else:
    print "Products CRITICAL : " + error_products + "missing products"
