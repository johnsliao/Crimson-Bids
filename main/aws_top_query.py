import base64, hashlib, hmac, time
from urllib import urlencode, quote_plus
import requests
from lxml import etree, html, objectify
import time

root_nodes = []

with open('./browsenodesid.txt','r') as f:
    for line in f:
        root_nodes = (line).split(',')

proxies = {
    "http": "http://usjli:atlantis590%23@proxyusbo.astratech.net:8080/",
}

def get_review(ASIN): # returns average rating, # feedback
    
    url = 'http://www.amazon.com/gp/customer-reviews/widgets/average-customer-review/popover/ref=dpx_acr_pop_?contextId=dpx&asin='+ASIN
    
    xml = requests.get(url, proxies=proxies)
    root = etree.fromstring(xml.text)
    avg_stars = '6'
    num_reviews = '6'

    for element in root.iter():
        if element.text is None:
            continue
        if "out of" in element.text:
            avg_stars = element.text.split()[0]
                    
        if "See all" in element.text:
            num_reviews = element.text.strip().split()[2]

    return avg_stars, num_reviews.replace(',','')

def amazon_test_url(nodeId):
    AWS_ACCESS_KEY_ID = 'AKIAIX7JH27EYWIW4F3Q'
    AWS_SECRET_ACCESS_KEY = 'UhGUzcSVu0S9k+B+enmo5prA6e4LWrV+3WrbA6Ox'

    base_url = "http://ecs.amazonaws.com/onca/xml"
    url_params = dict(
        Service='AWSECommerceService',
        Operation='BrowseNodeLookup',
        BrowseNodeId=nodeId,
        AWSAccessKeyId=AWS_ACCESS_KEY_ID,
        AssociateTag='johlia-20',
        ResponseGroup='TopSellers')

    # Add a ISO 8601 compliant timestamp (in GMT)
    url_params['Timestamp'] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    # Sort the URL parameters by key
    keys = url_params.keys()
    keys.sort()
    # Get the values in the same order of the sorted keys
    values = map(url_params.get, keys)

    # Reconstruct the URL parameters and encode them
    url_string = urlencode(zip(keys,values))

    #Construct the string to sign
    string_to_sign = "GET\necs.amazonaws.com\n/onca/xml\n%s" % url_string

    # Sign the request
    signature = hmac.new(
        key=AWS_SECRET_ACCESS_KEY,
        msg=string_to_sign,
        digestmod=hashlib.sha256).digest()

    # Base64 encode the signature
    signature = base64.encodestring(signature).strip()

    # Make the signature URL safe
    urlencoded_signature = quote_plus(signature)
    url_string += "&Signature=%s" % urlencoded_signature

    #print "%s?%s\n\n%s\n\n%s" % (base_url, url_string, urlencoded_signature, signature)
    return "%s?%s" % (base_url, url_string)

def browse_nodes(nodeId):
    AWS_ACCESS_KEY_ID = 'AKIAIX7JH27EYWIW4F3Q'
    AWS_SECRET_ACCESS_KEY = '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'

    base_url = "http://ecs.amazonaws.com/onca/xml"
    url_params = dict(
        Service='AWSECommerceService',
        Operation='BrowseNodeLookup',
        BrowseNodeId=nodeId,
        AWSAccessKeyId=AWS_ACCESS_KEY_ID,
        AssociateTag='johlia-20')

    # Add a ISO 8601 compliant timestamp (in GMT)
    url_params['Timestamp'] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    # Sort the URL parameters by key
    keys = url_params.keys()
    keys.sort()
    # Get the values in the same order of the sorted keys
    values = map(url_params.get, keys)

    # Reconstruct the URL parameters and encode them
    url_string = urlencode(zip(keys,values))

    #Construct the string to sign
    string_to_sign = "GET\necs.amazonaws.com\n/onca/xml\n%s" % url_string

    # Sign the request
    signature = hmac.new(
        key=AWS_SECRET_ACCESS_KEY,
        msg=string_to_sign,
        digestmod=hashlib.sha256).digest()

    # Base64 encode the signature
    signature = base64.encodestring(signature).strip()

    # Make the signature URL safe
    urlencoded_signature = quote_plus(signature)
    url_string += "&Signature=%s" % urlencoded_signature

    #print "%s?%s\n\n%s\n\n%s" % (base_url, url_string, urlencoded_signature, signature)
    return "%s?%s" % (base_url, url_string)

with open('./findings.csv', 'a') as f:
        f.write('average rating,num reviews, title, category\n')
        
for root_node in root_nodes:
    p_list_url = amazon_test_url(root_node)
    print p_list_url
    xml = requests.get(p_list_url, proxies=proxies)
    root = etree.fromstring(xml.text)

    flag = False
    category = ''
    
    for element in root.iter():
        if "Name" in element.tag and "Argument" not in element.tag:
            category = element.text
            
        if "ASIN" in element.tag:
            avg_stars, num_reviews = get_review(element.text)
            if avg_stars == 0:
                continue
            
            if float(avg_stars)<4.0 and int(num_reviews) < 500:
                with open('./findings.csv', 'a') as f:
                    f.write(avg_stars.encode('utf8')+',')
                    f.write(num_reviews.encode('utf8')+',')
                    
                flag = True
            
        if "Title" in element.tag:
            if flag:
                with open('./findings.csv', 'a') as f:
                    f.write(element.text.replace(',','').encode('utf8')+','+category.encode('utf8')+'\n')
            flag = False
























