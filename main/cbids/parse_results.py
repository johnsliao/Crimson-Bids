#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import petersMachine

from construct_url import Construct_URL
from lxml import etree, html
from dictionaries_lookup import iPhone
from inventory import Inventory
from boto.dynamodb2.table import Table
from boto.dynamodb2.items import Item
from datetime import datetime

class Query:

    def __init__(self):
        self.viable_products = []

    def parse_listing(self):
        u = Construct_URL()
        items = []

        for page in range(1,2):
            print 'looking at eBay page', page
            url = u.iPhone_listings(str(page))
            xml = requests.get(url)

            formatted_xml = xml.text.replace("<?xml version='1.0' encoding='UTF-8'?>",'')
            formatted_xml = formatted_xml.replace(' xmlns="http://www.ebay.com/marketplace/search/v1/services"', '')

            root = etree.fromstring(formatted_xml)

            searchResults = root.find('searchResult')
            items.append(searchResults)

        return items

    def search_NameValueList(self, item, missing_attribute):
        u = Construct_URL()
        itemId = self.get_itemId(item)
        url = u.single_product(itemId)
        xml = requests.get(url)

        formatted_xml = xml.text.replace('<?xml version="1.0" encoding="UTF-8"?>','')
        formatted_xml = formatted_xml.replace(' xmlns="urn:ebay:apis:eBLBaseComponents"', '')
        root = etree.fromstring(formatted_xml)

        item = root.find('Item')
        ItemSpecifics = item.find('ItemSpecifics')
        NameValueList = ItemSpecifics.findall('NameValueList')

        for NameValue in NameValueList:
            Name = NameValue.find('Name')

            if Name.text == missing_attribute:
                Value = NameValue.find('Value')
                return Value.text

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
        endTime = listingInfo.find('endTime')

        # sellingStatus
        sellingStatus = item.find('sellingStatus')
        currentPrice = sellingStatus.find('currentPrice')
        bidCount = sellingStatus.find('bidCount')
        timeLeft = sellingStatus.find('timeLeft')

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
            timeLeft.text,
            endTime.text
        ]

    def rough_check(self, item):
        # title
        title = item.find('title')

        # sellerInfo
        sellerInfo = item.find('sellerInfo')
        positiveFeedbackPercent = sellerInfo.find('positiveFeedbackPercent')
        feedbackRatingStar = sellerInfo.find('feedbackRatingStar')

        # Quality Requirements
        if float(positiveFeedbackPercent.text) < 95:
            return False
        if feedbackRatingStar.text == 'None':
            return False

        return True

    def run_peters_machine(self, item): # go to specific listing and check sellerNotes via scraper

        url = self.get_itemURL(item)
        url = url.replace('\n', '')
        page = requests.get(url)

        tree = html.fromstring(page.text)

        sellerNotes = tree.xpath('//span[@class="viSNotesCnt"]/text()')

        if len(sellerNotes) == 0:
            sellerNotes = ''
        else:
            sellerNotes = sellerNotes[0]

        description = self.get_description(item)

        if description is None:
            description = 'null'


        # Run through Peters machine
        text = description.lower() + '.' + sellerNotes.lower() # append seller notes to description...
        text = text.encode('utf8')

        print text

        dictionary = petersMachine.Dictionary(text)
        dictionary.pushThroughIphoneMachine()

        result = dictionary.IPhoneDictionary.IPhoneVault.getStatus() # should return structured data

        # Return True/False based on findings
        return result

    def add_to_db(self):
        items_table = Table('items')

        for product in self.viable_products:
            temp_item = Item(items_table, data={
                'type':'iphone',
                'title':product[0],
                'itemId':product[1],
                'viewItemURL':product[2],
                'sellerUserName':product[3],
                'positiveFeedbackPercent':product[4],
                'feedbackRatingStar':product[5],
                'conditionId':product[6],
                'listingType':product[7],
                'currentPrice':product[8],
                'bidCount':product[9],
                'timeLeft':product[10],
                'endTime':product[11],
                'carrier':product[12],
                'storage':product[13],
                'model':product[14],
                'color':product[15],
                'pmresult':product[16],
            })

            temp_item.save(overwrite=True)

        print 'all set'

    def get_description(self, item):  # for specific product
        u = Construct_URL()
        itemId = self.get_itemId(item)
        url = u.single_product(itemId)
        xml = requests.get(url)

        formatted_xml = xml.text.replace('<?xml version="1.0" encoding="UTF-8"?>','')
        formatted_xml = formatted_xml.replace(' xmlns="urn:ebay:apis:eBLBaseComponents"', '')
        root = etree.fromstring(formatted_xml)

        item = root.find('Item')
        Description = item.find('Description')

        if Description is None:
            return ('DNE')

        if Description is not None:
            print 'Entered Description'
            return Description.text

    def get_title(self, item):
        title = item.find('title')
        return title.text

    def get_itemId(self, item):
        itemId = item.find('itemId')
        return itemId.text

    def get_itemURL(self, item):
        viewItemURL = item.find('viewItemURL')
        return viewItemURL.text

    def get_listing_type(self, item):
        listingInfo = item.find('listingInfo')
        listingType = listingInfo.find('listingType')
        return listingType.text


if __name__ == '__main__':
    #path1 = '//var//www//lighttpd//cgi-bin//product_list.txt'
    path1 = '//users//johnliao//dropbox//crimson bids//main//product_list.txt'

    print 'Create inventory object'
    inventory = Inventory()

    print 'Create iPhone dictionary'
    iPhone_dict = iPhone()

    print 'Populate product listings'
    inventory.import_product_list(path1)

    print 'Parse eBay xml'
    q = Query()
    items_array = q.parse_listing()

    print 'Add to inventory'
    (identified, total, unidentified, roughReject, p_likenew, p_forparts, num_auctions) = (0, 0, 0, 0,0,0, 0)


    DNE_attributes = ['CARRIER-DNE', 'STORAGE-DNE', 'MODEL-DNE','COLOR-DNE']

    for items in items_array:
        for item in items:
            total += 1
            rtitle = q.get_title(item)
            title = iPhone_dict.check_title_attributes(rtitle)
            print '''----------- \nCurrently analyzing...''', rtitle

            if item is None:
                continue

            for word in enumerate(title):  # refined check using GetSingleItem()
                if any(attribute in word[1] for attribute in DNE_attributes):

                    if 'CARRIER-DNE' in word[1]:
                        title[word[0]] = q.search_NameValueList(item,'Carrier')
                    if 'STORAGE-DNE' in word[1]:
                        title[word[0]] = q.search_NameValueList(item,'Storage Capacity')
                    if 'MODEL-DNE' in word[1]:
                        title[word[0]] = q.search_NameValueList(item,'Model')
                    if 'COLOR-DNE' in word[1]:
                        title[word[0]] = q.search_NameValueList(item,'Color')

            if q.rough_check(item) is False:
                roughReject += 1
                continue

            if inventory.retrieve_productid(title) == -1:
                print 'Reject! Unable to identify!\n'
                unidentified += 1
                continue

            identified += 1
            peters_machine_result = []

            if q.run_peters_machine(item) is True: # run peters machine here
                p_likenew += 1
                peters_machine_result.append('like-new')
            if q.run_peters_machine(item) is False: # run peters machine here
                p_forparts += 1
                peters_machine_result.append('for-parts')

            if 'auction' in q.get_listing_type(item).lower():
                num_auctions += 1

            more_info = q.get_product_information(item)
            all_info = more_info + title + peters_machine_result

            q.viable_products.append(all_info)

    print "\n***** RESULTS ******\n"
    print '# products identified:', identified
    print '# items unidentified:', unidentified
    print '# Rough check reject count', roughReject
    print '# Auctions', num_auctions
    print '# Total items:', total

    print '\n# Peter Like New count', p_likenew
    print '\n# Peter For Parts count', p_forparts

    print "\n*****FINISHED WITH EBAY API******\n"

    #fname = '//var//www//lighttpd//cgi-bin//parse_history//parse_history.txt'
    fname = '//test.txt'
    time = datetime.now().strftime('%Y-%m-%d__%H:%M:%S')

    with open(fname,'a') as f:
        f.writelines(time)

        f.writelines('\n')

        f.writelines('# products identified: '+str(identified))

        f.writelines('\n')

        f.writelines('# items unidentified: '+str(unidentified))

        f.writelines('\n')

        f.writelines('# Rough check reject count '+str(roughReject))

        f.writelines('\n')

        f.writelines('# Auctions: '+str(num_auctions))

        f.writelines('\n')

        f.writelines('# Total items: '+str(total))

        f.writelines('\n')

        f.writelines('# Peter Like New count: '+str(p_likenew))

        f.writelines('\n')

        f.writelines('# Peter For Parts count: '+str(p_forparts))

        f.writelines('\n')

        f.writelines('---------------------------------------------------')

        f.writelines('\n\n')

    #print 'add products to dynamoDB'
    #q.add_to_db()

    print "finished"