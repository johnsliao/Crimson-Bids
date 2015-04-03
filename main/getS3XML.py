import sys
import os
import cgi

from lxml import etree, html

class xml:
    def __init__(self, model, carrier, storage, color):
        self.itemRoots = []
        self.model = model
        self.carrier = carrier
        self.storage = storage
        self.color = color

    def appendItemTree(self, fpath):
        dom = etree.parse(fpath)
        root = dom.getroot()

        self.itemRoots.append(root)

    def parseXML(self):
        viable_products = []
        columns = [
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
            'timeLeft',
            'carrier',
            'storage',
            'model',
            'color'
        ]

        for itemRoot in self.itemRoots:
            for item in itemRoot:

                title = item.find('title')
                itemId = item.find('itemId')
                viewItemURL = item.find('viewItemURL')
                sellerUserName = item.find('sellerUserName')
                positiveFeedbackPercent = item.find('positiveFeedbackPercent')
                feedbackRatingStar = item.find('feedbackRatingStar')
                conditionId = item.find('conditionId')
                listingType = item.find('listingType')
                currentPrice = item.find('currentPrice')
                bidCount = item.find('bidCount')
                timeLeft = item.find('timeLeft')
                carrier = item.find('carrier')
                storage = item.find('storage')
                model = item.find('model')
                color = item.find('color')

                if model.text != self.model:
                    continue
                if carrier.text != self.carrier:
                    continue
                if storage.text != self.storage:
                    continue
                if color.text != self.color:
                    continue

                viable_products.append([title.text, itemId.text, viewItemURL.text,
                                          sellerUserName.text, positiveFeedbackPercent.text,
                                          feedbackRatingStar.text, conditionId.text, listingType.text,
                                          currentPrice.text, bidCount.text, timeLeft.text, carrier.text,
                                          storage.text, model.text, color.text])

            root = etree.Element("root")
            item = []

            itemCount = 0
            count = 0

            for product in viable_products:
                item.append(etree.SubElement(root, "item"))
                count = 0
                for p in product:
                    entry = ''
                    entry = etree.SubElement(item[itemCount], columns[count])
                    entry.text = str(p)
                    count += 1
                itemCount += 1

            xslt_root = etree.parse(r'./xsl_file.xsl')
            transform = etree.XSLT(xslt_root)

            et = etree.ElementTree(root)
            et = transform(et)
            print et
            et.write('./parsed_productsXML.html')


def main():
    form = cgi.FieldStorage()
    model = form["model"].value.upper()
    carrier = form["carrier"].value.upper()
    storage = form["storage"].value.upper()
    color = form["color"].value.upper()

    x = xml(model, carrier, storage, color)

    x.appendItemTree(r'./copiedFromS3.xml')

    x.parseXML()

if __name__ == '__main__':
    main()