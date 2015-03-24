def ebaytime_to_time(self, etime):
    # eBay time format: P3DT4H35M42S
    
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

def parse(self):
    entry = 'itemId, title, sellerUserName, positiveFeedbackPercent, feedbackRatingStar, conditionId, listingType, currentPrice, url, days, hours, minutes, seconds \n'

    dom = etree.parse(self.fname)
    root = dom.getroot()

    searchResults = root.find('searchResult')
    items = searchResults

    for item in items:

        # itemId
        itemId = item.find('itemId')

        # title
        title = item.find('title')
        
        attributes = iPhone_dictionary(title.text) # Look up what inventory bucket listing goes into
        self.populate_product_inventory(attributes,title.text)
        
        # viewItemURL
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
        timeLeft = sellingStatus.find('timeLeft')

        entry += itemId.text + ','
        entry += title.text.replace(',',' ').strip() + ',' # \n at the beginning, remove ','
        entry += sellerUserName.text + ','
        entry += positiveFeedbackPercent.text + ','
        entry += feedbackRatingStar.text + ','
        entry += conditionId.text + ','
        entry += listingType.text + ','
        entry += currentPrice.text + ','
        entry += viewItemURL.text.strip() + ',' # \n at the beginning of viewItemURL
        entry += self.ebaytime_to_time(timeLeft.text) + ','
        entry += '\n'

    #print entry
