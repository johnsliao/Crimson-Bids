import time

from boto.dynamodb2.fields import HashKey, RangeKey, GlobalAllIndex
from boto.dynamodb2.table import Table
from boto.dynamodb2.types import NUMBER

def main():
    print 'checking endtimes...'

    items_table = Table('items')
    usr_itemQuery = items_table.scan()

    for usr_item in usr_itemQuery:
        endTime = usr_item['endTime']

        if endTime is None:
            print 'nonetype listing! deleting...'
            usr_item.delete()

            continue

        list_date, list_time = (endTime.encode('utf-8').decode('ascii', 'ignore')).split('T')

        list_time = list_time.replace('.000Z','')

        if list_date>time.strftime("%Y/%m/%d"):
            print 'current date is:', time.strftime("%Y/%m/%d")
            print 'listing date is:', list_date
            print 'expired listing by date! deleting...'
            usr_item.delete()
            continue

        if list_time>time.strftime("%H:%M:%S"):
            print 'current time is:', time.strftime("%H:%M:%S")
            print 'listing time is:', list_time
            print 'expired listing by time! deleting...'
            usr_item.delete()
            continue

    print 'finished'

if __name__ == '__main__':
    main()
