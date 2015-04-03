import sys
import os
import cgi

from boto.dynamodb2.fields import HashKey, RangeKey, GlobalAllIndex
from boto.dynamodb2.table import Table
from boto.dynamodb2.types import NUMBER

def main():
    # form = cgi.FieldStorage()
    # model = form["model"].value.upper()
    # carrier = form["carrier"].value.upper()
    # storage = form["storage"].value.upper()
    # color = form["color"].value.upper()
    items_table = Table('items')

    ATT_listings = items_table.scan(carrier__eq='ATT')

    for list in ATT_listings:
        print list['itemId']

    print 'done'

if __name__ == '__main__':
    main()
