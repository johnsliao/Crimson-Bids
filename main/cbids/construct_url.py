from lxml import etree
import requests


class Construct_URL():
    def __init__(self):
        #self.MY_APP_ID = 'CrimsonB-770e-4f72-969a-a59a85341b09' # Sandbox
        self.MY_APP_ID = 'CrimsonB-2aa7-4264-8615-558696ab4616' # Production
        self.OPERATION_NAME = 'findItemsByProduct'
        self.SERVICE_VERSION = '1.0.0'
        self.RESPONSE_DATA_FORMAT = 'XML'
        self.PRODUCT_TYPE = 'UPC'
        self.PRODUCT_ID = '885909772148' # UPC
        self.ITEM_FILTER = 'ListingType'
        self.ITEM_FILTER_VALUE = 'Auction'
        #self.ITEM_FILTER_VALUE = 'FixedPrice', 'AuctionWithBIN'
        self.SORT_ORDER = 'PricePlusShippingLowest'

    def iPhone_listings(self, pageNumber):
        #iPhone with Pagination
        url = ['http://svcs.ebay.com/services/search/FindingService/v1?OPERATION-NAME=findItemsAdvanced&SERVICE-VERSION=1.0.0',
               '&SECURITY-APPNAME=',self.MY_APP_ID,'&RESPONSE-DATA-FORMAT=XML&REST-PAYLOAD',
               '&paginationInput.entriesPerPage=100',
               '&paginationInput.pageNumber=',str(pageNumber),
               '&keywords=iPhone&categoryId=9355&descriptionSearch=true&outputSelector=SellerInfo']
        address = ''
        for u in url:
            address += u

        return address


    def single_product(self, itemId):
        url = ''
        url += 'http://open.api.ebay.com/shopping?'
        url += 'callname=GetSingleItem'
        url += '&responseencoding=XML&'
        url += 'appid=' + self.MY_APP_ID
        url += '&siteid=0&version=515'
        url += '&ItemID=' + itemId
        url += '&IncludeSelector=Details,TextDescription,ItemSpecifics,ConditionDescription'

        return url

def main():
    c = Construct_URL()
    url = c.single_product('371299724415')
    print url
    url = c.iPhone_listings(1)
    print url

if __name__ == '__main__':
    main()