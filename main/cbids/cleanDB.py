from datetime import datetime

from boto.dynamodb2.fields import HashKey, RangeKey, GlobalAllIndex
from boto.dynamodb2.table import Table
from boto.dynamodb2.types import NUMBER

def main():
    print 'starting cleanDB.py...'
    
    items_table = Table('items')
    
    usr_itemQuery = items_table.scan()

    for usr_item in usr_itemQuery:
        endTime = usr_item['endTime']

        if endTime is None:
            print 'nonetype listing! deleting...'
            usr_item.delete()
            continue
        
        now = datetime.utcnow()
        list_date, list_time = (endTime.encode('utf-8').decode('ascii', 'ignore')).split('T')
        list_time = list_time.replace('.000Z','')
        
        together = list_date+list_time

        c_end_time = datetime.strptime(together, '%Y-%m-%d%H:%M:%S')
        
        diff = c_end_time - now
        
        diff = diff.total_seconds()

        if diff < 0:
            print 'expired listing by time! deleting...'
            usr_item.delete()
            continue

    print 'finished'

if __name__ == '__main__':
    main()
