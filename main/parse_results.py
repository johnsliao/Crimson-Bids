#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
import requests

from construct_url import Construct_URL
from lxml import etree, html
from dictionaries_lookup import iPhone
from inventory import Inventory

SEARCH_MODE = 'LIVE'

#SEARCH_MODE = 'XML'


class Query:

    def __init__(self):
        self.screenout_keywords = [
            'BAD',
            'POOR',
            'CRACK',
            'BROKEN',
            'SCRATCH',
            'CHIP',
            'DENT',
            'SCUFF',
            'DAMAGE',
            'DROP',
            'BROKE',
        ]
        self.viable_products = [
            'title',
            'itemId',
            'viewItemURL',
            'sellerUserName',
            'positiveFeedbackPercent',
            'feedbackRatingStar',
            'conditionId',
            'listingType',
            'currentPrice',
            'bidCount',
            'days',
            'hours',
            'mins',
            'sec',
        ]

    def parse_listing(self, path):
        global SEARCH_MODE

        if SEARCH_MODE == 'XML':
            dom = etree.parse(path)
            root = dom.getroot()
        if SEARCH_MODE == 'LIVE':
            u = Construct_URL()
            url = u.iPhone_listings(1)
            xml = requests.get(url)
            formatted_xml = xml.text.replace("<?xml version='1.0' encoding='UTF-8'?>",'')
            formatted_xml = formatted_xml.replace(' xmlns="http://www.ebay.com/marketplace/search/v1/services"', '')
            root = etree.fromstring(formatted_xml)

        searchResults = root.find('searchResult')
        items = searchResults

        return items

    def parse_single_product(self, item):
        u = Construct_URL()
        itemId = self.get_itemId(item)
        url = u.single_product(itemId)
        xml = requests.get(url)

        formatted_xml = xml.text.replace('<?xml version="1.0" encoding="UTF-8"?>','')
        formatted_xml = formatted_xml.replace(' xmlns="urn:ebay:apis:eBLBaseComponents"', '')
        root = etree.fromstring(formatted_xml)

        save_product_xml(root)

    def search_NameValueList(self, item, missing_attribute):
        itemId = self.get_itemId(item)
        path = r'/users/johnliao/temp/' + itemId + '.xml'
        dom = etree.parse(path)
        root = dom.getroot()

        item = root.find('Item')
        ItemSpecifics = item.find('ItemSpecifics')
        NameValueList = ItemSpecifics.findall('NameValueList')

        for NameValue in NameValueList:
            Name = NameValue.find('Name')

            # print 'Currently comparing:', Name.text, 'to', missing_attribute

            if Name.text == missing_attribute:
                Value = NameValue.find('Value')

                # print 'Found deeper listing!', Value.text

                return Value.text

        # print 'Did not find anything :('

        return missing_attribute

    def get_product_information(self, item):  # get info for viable product

        # title

        title = item.find('title')

        # itemId

        itemId = item.find('itemId')

        # itemURL

        viewItemURL = item.find('viewItemURL')

        # sellerInfo

        sellerInfo = item.find('sellerInfo')
        sellerUserName = sellerInfo.find('sellerUserName')
        positiveFeedbackPercent = sellerInfo.find('positiveFeedbackPercent')
        feedbackRatingStar = sellerInfo.find('feedbackRatingStar')

        # condition

        condition = item.find('condition')
        conditionId = condition.find('conditionId')

        # listingInfo

        listingInfo = item.find('listingInfo')
        listingType = listingInfo.find('listingType')

        # sellingStatus

        sellingStatus = item.find('sellingStatus')
        currentPrice = sellingStatus.find('currentPrice')
        bidCount = sellingStatus.find('bidCount')
        eBayTimeLeft = sellingStatus.find('timeLeft')
        timeLeft = self.ebaytime_to_time(eBayTimeLeft.text)

        if bidCount is None:
            bidCount = 0
        else:
            bidCount = bidCount.text

        return [
            title.text.replace(',', ''),
            itemId.text,
            viewItemURL.text.replace(',', ''),
            sellerUserName.text,
            positiveFeedbackPercent.text,
            feedbackRatingStar.text,
            conditionId.text,
            listingType.text,
            currentPrice.text,
            bidCount,
            timeLeft,
        ]

    def check_quality(self, item):

        # title

        title = item.find('title')

        # sellerInfo

        sellerInfo = item.find('sellerInfo')
        sellerUserName = sellerInfo.find('sellerUserName')
        positiveFeedbackPercent = sellerInfo.find('positiveFeedbackPercent')
        feedbackRatingStar = sellerInfo.find('feedbackRatingStar')

        # condition

        condition = item.find('condition')
        conditionId = condition.find('conditionId')

        # listingInfo

        listingInfo = item.find('listingInfo')
        listingtype = listingInfo.find('listingType')

        # sellingStatus

        sellingStatus = item.find('sellingStatus')
        currentPrice = sellingStatus.find('currentPrice')
        timeLeft = sellingStatus.find('timeLeft')

        # Quality Requirements

        if float(positiveFeedbackPercent.text) < 95:
            print 'Reject!', positiveFeedbackPercent.text
            return False
        if feedbackRatingStar.text == 'None':
            print 'Reject!', feedbackRatingStar.text
            return False
        if int(conditionId.text) > 3000:  # Worse than Used
            print 'Reject!', conditionId.text
            return False

        for word in self.screenout_keywords:
            if word in title.text.upper().split():
                print 'Reject!', word
                return False

        return True

    def check_description_quality(self, item):

        # go to specific listing and check sellerNotes via scraper

        url = self.get_itemURL(item)
        url = url.replace('\n', '')
        page = requests.get(url)

        tree = html.fromstring(page.text)

        sellerNotes = tree.xpath('//span[@class="viSNotesCnt"]/text()')
        if not len(sellerNotes) == 0:
            print sellerNotes

            sellerNotes = sellerNotes[0].split()

            for word in sellerNotes:
                for screenout_keyword in self.screenout_keywords:
                    if screenout_keyword in word.upper():
                        print 'Reject! SellerNotes screenout keyword activated:', word
                        return False

        for word in self.get_description(item):
            for screenout_keyword in self.screenout_keywords:

                    # print 'comparing ', word.upper(),'TO', screenout_keyword

                if screenout_keyword in word.upper():
                    print self.get_description(item)
                    print 'Reject! Description screenout keyword activated:', word
                    return False

        return True

    def ebaytime_to_time(self, etime):  # eBay time format: P3DT4H35M42S
        time = ''
        seg = ''
        for char in etime:
            if not char.isdigit():
                if not seg == '':
                    time += seg
                    time += ','
                seg = ''
                continue
            seg += char

        return time

    def export_viable_products(self):
        fname = '/users/johnliao/temp/Viable_products.csv'

        # fname = r'C:/Temp/Viable_products.csv'

        with open(fname, 'w') as fs:
            for product in self.viable_products:

                # print 'product, ',product

                text = ''
                for attribute in product:

                    # print text

                    text += str(attribute).replace('\n', '')
                    text += ','
                text += '\n'
                fs.write(text)

    def get_title(self, item):
        title = item.find('title')

        return title.text

    def get_itemId(self, item):
        itemId = item.find('itemId')

        return itemId.text

    def get_itemURL(self, item):

        # itemURL

        viewItemURL = item.find('viewItemURL')
        return viewItemURL.text

    def get_conditionId(self, item):

        # condition

        condition = item.find('condition')
        conditionId = condition.find('conditionId')

        return conditionId.text

    def get_listingType(self, item):
        listingInfo = item.find('listingInfo')
        listingType = listingInfo.find('listingType')

        return listingType.text

    def get_description(self, item):  # for specific product
        itemId = self.get_itemId(item)
        path = r'/users/johnliao/temp/' + itemId + '.xml'
        dom = etree.parse(path)
        root = dom.getroot()

        item = root.find('Item')
        Description = item.find('Description')

        if not Description == None:
            return Description.text.split()

        return (-1)


def save_product_xml(tree):
    item = tree.find('Item')
    itemId = item.find('ItemID')
    fname = r'/users/johnliao/temp/' + itemId.text + '.xml'

    # fname = r'C:/Temp/Viable_products.csv'

    xml = etree.tostring(tree, pretty_print=True)
    with open(fname, 'w') as fs:
        for line in xml:
            fs.write(line)


if __name__ == '__main__':
    if SEARCH_MODE == 'XML':
        if not len(sys.argv) == 3:
            print 'Usage', sys.argv[0], '[PRODUCT LISITINGS] [EBAY LISTINGS]'
            sys.exit(0)

        path1 = sys.argv[1]
        path2 = sys.argv[2]

        if not os.path.exists(path1) or not os.path.exists(path2):
            print 'Could not find', path1, path2
            sys.exit(0)

    if SEARCH_MODE == 'LIVE':
        if not len(sys.argv) == 2:
            print 'Usage', sys.argv[0], '[PRODUCT LISITINGS]'
            sys.exit(0)

        path1 = sys.argv[1]
        path2 = ''

        if not os.path.exists(path1):
            print 'Could not find', path1
            sys.exit(0)

    # Create inventory object

    inventory = Inventory()

    # Create iPhone dictionary

    iPhone_dict = iPhone()

    # Populate product listings

    inventory.import_product_list(path1)

    # Parse eBay xml

    q = Query()
    items = q.parse_listing(path2)

    # Add to inventory

    (identified, reject, total, unidentified, auctions) = (0, 0, 0, 0,0)
    DNE_attributes = ['CARRIER-DNE', 'STORAGE-DNE', 'MODEL-DNE','COLOR-DNE']

    for item in items:
        total += 1
        rtitle = q.get_title(item)
        title = iPhone_dict.check_title_attributes(rtitle)
        print '''----------- '''
        print 'Currently analyzing...', rtitle

        for word in enumerate(title):  # refined check using GetSingleItem()
            if any(attribute in word[1] for attribute in DNE_attributes):
                q.parse_single_product(item)

                if 'CARRIER-DNE' in word[1]:
                    title[word[0]] = q.search_NameValueList(item,'Carrier')
                if 'STORAGE-DNE' in word[1]:
                    title[word[0]] = q.search_NameValueList(item,'Storage Capacity')
                if 'MODEL-DNE' in word[1]:
                    title[word[0]] = q.search_NameValueList(item,'Model')
                if 'COLOR-DNE' in word[1]:
                    title[word[0]] = q.search_NameValueList(item,'Color')

        if q.check_quality(item) == False:
            reject += 1
            continue

        # read description if product is used
        if int(q.get_conditionId(item)) == 3000:
            q.parse_single_product(item)
            if q.check_description_quality(item) == False:
                reject += 1
                continue

        product_id = inventory.retrieve_productid(title)

        if product_id == -1:
            print 'Reject! Unable to identify! :c\n'
            unidentified += 1
            continue

        identified += 1

        if 'Auction' in q.get_listingType(item):
            auctions += 1

        print 'Accept! Good product! C:\n'
        more_info = q.get_product_information(item)
        inventory.add_inventory(product_id)

        q.viable_products.append(more_info)

    print '# Total items:', total
    print '# products identified and put into Inventory:', identified
    print '# items unidentified:', unidentified
    print '# items rejected:', reject
    print 'Inventory products/Total:', float(identified) / float(total) * 100, '%'
    print 'Total viable products [%]:', float(identified) / float(total) * 100, '%'
    print '# auctions:', auctions

    # Save xml to directory

    q.export_viable_products()

    # inventory.export_inventory()
