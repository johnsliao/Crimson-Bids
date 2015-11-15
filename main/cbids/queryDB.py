import sys
import os
import simplejson as json
import time
from datetime import datetime

from lxml import etree, html
from boto.dynamodb2.fields import HashKey, RangeKey, GlobalAllIndex
from boto.dynamodb2.table import Table
from boto.dynamodb2.types import NUMBER

def convertConditionId(conditionId):
    if (conditionId == '1000'):
        return 'New'
    if (conditionId == '1500'): #"new other"
        return 'New'
    if (conditionId == '1750'): #"New with defects"
        return 'New'
    if (conditionId == '2000'):
        return 'Refurbished'
    if (conditionId == '2500'):
        return 'Refurbished'
    if (conditionId == '3000'):
        return 'Used'

def simplifyTime(endTime):
    now = datetime.utcnow()

    list_date, list_time = (endTime.encode('utf-8').decode('ascii', 'ignore')).split('T')
    list_time = list_time.replace('.000Z','')

    together = list_date+list_time

    c_end_time = datetime.strptime(together, '%Y-%m-%d%H:%M:%S')

    diff = c_end_time - now

    diff = diff.total_seconds()

    return diff


def checkExpired(endTime):
        if endTime is None:
            print 'nonetype listing! deleting...'
            return True

        now = datetime.utcnow()
        list_date, list_time = (endTime.encode('utf-8').decode('ascii', 'ignore')).split('T')
        list_time = list_time.replace('.000Z','')

        together = list_date+list_time

        c_end_time = datetime.strptime(together, '%Y-%m-%d%H:%M:%S')

        diff = c_end_time - now

        diff = diff.total_seconds()

        if diff < 0:
            print 'expired listing by time! deleting...'
            return True

        return False

def main():

    items_table = Table('items')

    usr_itemQuery = items_table.scan()

    iphone6p = []
    iphone6 = []
    iphone5s = []
    iphone5c = []
    iphone5 = []
    iphone4s = []
    iphone4 = []

    for usr_item in usr_itemQuery:
        title = usr_item['title']
        itemId = usr_item['itemId']
        viewItemURL = usr_item['viewItemURL']
        sellerUserName = usr_item['sellerUserName']
        positiveFeedbackPercent = usr_item['positiveFeedbackPercent']
        feedbackRatingStar = usr_item['feedbackRatingStar']
        conditionId = usr_item['conditionId']
        listingType = usr_item['listingType']
        currentPrice = usr_item['currentPrice']
        bidCount = usr_item['bidCount']
        timeLeft = usr_item['timeLeft']
        endTime = usr_item['endTime']
        carrier = usr_item['carrier']
        color = usr_item['color']
        storage = usr_item['storage']
        model = usr_item['model']
        pmresult = usr_item['pmresult']

        if checkExpired(endTime):
            continue

        # CREATE JSON

        item = {}

        item['title'] = title
        item['itemId'] = '''<a target="_blank" href="http://rover.ebay.com/rover/1/711-53200-19255-0/1?icep_ff3=2&pub=5575124864&toolid=10001&campid=5337694064&customid=&icep_item='''+itemId+'''&ipn=psmain&icep_vectorid=229466&kwid=902099&mtid=824&kw=lg">'''+itemId+'''</a>'''
        item['viewItemURL'] = viewItemURL
        item['sellerUserName'] = sellerUserName
        item['positiveFeedbackPercent'] = positiveFeedbackPercent
        item['feedbackRatingStar'] = feedbackRatingStar
        item['conditionId'] = convertConditionId(conditionId)
        item['listingType'] = listingType
        item['currentPrice'] = '$'+str(currentPrice)
        item['bidCount'] = bidCount
        item['timeLeft'] = simplifyTime(endTime)
        item['endTime'] = endTime
        item['carrier'] = carrier
        item['color'] = color
        item['storage'] = storage
        item['model'] = model
        item['pmresult'] = pmresult
        item['bidnow'] = '<form action="./cgi-bin/single_item_grabber.py" method="get"> <button name="itemId" type="submit" value="'+itemId+'">view info</button></form>'

        if model == '6PLUS':
            if not any(d for d in iphone6p if itemId in d['itemId']):
                iphone6p.append(item)
        if model == '6':
            if not any(d for d in iphone6 if itemId in d['itemId']):
                iphone6.append(item)
        if model == '5S':
            if not any(d for d in iphone5s if itemId in d['itemId']):
                iphone5s.append(item)
        if model == '5C':
            if not any(d for d in iphone5c if itemId in d['itemId']):
                iphone5c.append(item)
        if model == '5':
            if not any(d for d in iphone5 if itemId in d['itemId']):
                iphone5.append(item)
        if model == '4S':
            if not any(d for d in iphone4s if itemId in d['itemId']):
                iphone4s.append(item)
        if model == '4':
            if not any(d for d in iphone4 if itemId in d['itemId']):
                iphone4.append(item)


    with open('//var//www//lighttpd//cgi-bin//iphone6p.json', 'w') as fs:
        json.dump(iphone6p,fs)
    with open('//var//www//lighttpd//cgi-bin//iphone6.json', 'w') as fs:
        json.dump(iphone6,fs)
    with open('//var//www//lighttpd//cgi-bin//iphone5s.json', 'w') as fs:
        json.dump(iphone5s,fs)
    with open('//var//www//lighttpd//cgi-bin//iphone5c.json', 'w') as fs:
        json.dump(iphone5c,fs)
    with open('//var//www//lighttpd//cgi-bin//iphone5.json', 'w') as fs:
        json.dump(iphone5,fs)
    with open('//var//www//lighttpd//cgi-bin//iphone4s.json', 'w') as fs:
        json.dump(iphone4s,fs)
    with open('//var//www//lighttpd//cgi-bin//iphone4.json', 'w') as fs:
        json.dump(iphone4,fs)

if __name__ == '__main__':
    main()
    #print simplifyTime('2015-04-30T12:00:00.000Z')
