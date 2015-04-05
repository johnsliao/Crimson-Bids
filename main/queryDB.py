import sys
import os
import cgi

from lxml import etree, html
from boto.dynamodb2.fields import HashKey, RangeKey, GlobalAllIndex
from boto.dynamodb2.table import Table
from boto.dynamodb2.types import NUMBER

def main():

    form = cgi.FieldStorage()
    model = form["model"].value.upper()
    carrier = form["carrier"].value.upper()
    storage = form["storage"].value.upper()
    color = form["color"].value.upper()
    items_table = Table('items')

    usr_itemQuery = items_table.scan(model__eq = model, storage__eq = storage, color__eq = color, carrier__eq=carrier)

    root = etree.Element("root")

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


        item = etree.SubElement(root, "item")

        xml_title_entry = etree.SubElement(item, "title")
        xml_title_entry.text = title

        xml_title_entry = etree.SubElement(item, "itemId")
        xml_title_entry.text = itemId

        xml_title_entry = etree.SubElement(item, "viewItemURL")
        xml_title_entry.text = viewItemURL

        xml_title_entry = etree.SubElement(item, "sellerUserName")
        xml_title_entry.text = sellerUserName

        xml_title_entry = etree.SubElement(item, "positiveFeedbackPercent")
        xml_title_entry.text = positiveFeedbackPercent

        xml_title_entry = etree.SubElement(item, "feedbackRatingStar")
        xml_title_entry.text = feedbackRatingStar

        xml_title_entry = etree.SubElement(item, "conditionId")
        xml_title_entry.text = conditionId

        xml_title_entry = etree.SubElement(item, "listingType")
        xml_title_entry.text = listingType

        xml_title_entry = etree.SubElement(item, "currentPrice")
        xml_title_entry.text = currentPrice

        xml_title_entry = etree.SubElement(item, "bidCount")
        xml_title_entry.text = str(bidCount)

        xml_title_entry = etree.SubElement(item, "timeLeft")
        xml_title_entry.text = timeLeft

        xml_title_entry = etree.SubElement(item, "endTime")
        xml_title_entry.text = endTime

    xslt_root = etree.parse(r'./xsl_file.xsl')
    transform = etree.XSLT(xslt_root)

    et = etree.ElementTree(root)
    et = transform(et)
    print et

if __name__ == '__main__':
    main()
