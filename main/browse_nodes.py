import base64, hashlib, hmac, time
from urllib import urlencode, quote_plus
import requests
from lxml import etree, html, objectify
from lxml.objectify import NoneElement
import time

root_nodes = [
    '2350149011',
    '283155',
    '133140011',
    '599858',
    '2625373011',
    '5174',
    '163856011',
    '468642',
    '172282',
    '2335752011',
    '2619525011',
    '11091801',
    '229534',
    '1064954',
    '1055398',
    '2972638011',
    '228013',
    '2617941011',
    '2619533011',
    '16310101',
    '3760901',
    '3760911',
    '165793011',
    '165796011',
    '1036592',
    '672123011',
    '3367581',
    '377110011',
    '3375251',
    '15684181',
    '16310091',]

proxies = {
    "http": "http://usjli:atlantis590%23@proxyusbo.astratech.net:8080/",
}

def get_url(nodeId):
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

def pull_node(url): # returns average rating, # feedback
    xml = requests.get(url, proxies=proxies)
    f_xml = xml.text.replace('http://webservices.amazon.com/AWSECommerceService/2011-08-01','')
    root = etree.fromstring(f_xml)
    print f_xml
    
    Children = root.find('.//Children')

    if isinstance(Children, NoneElement) or Children is None:
        return 0

    BrowseNodeIds = Children.findall('.//BrowseNodeId')
    
    for element in BrowseNodeIds:
        master_nodes.append(element.text)

def first_node(url): # returns average rating, # feedback
    xml = requests.get(url, proxies=proxies)
    f_xml = xml.text.replace('http://webservices.amazon.com/AWSECommerceService/2011-08-01','')
    root = etree.fromstring(f_xml)
    
    Children = root.find('.//Children')
    if isinstance(Children, NoneElement) or Children is None:
        return
    
    BrowseNodeIds = Children.findall('.//BrowseNodeId')

    for element in BrowseNodeIds:
        cat_nodes.append(element.text)
    
master_nodes = []
cat_nodes = []

for root_node in root_nodes:
    cat_nodes = []
    url = get_url(root_node)
    first_node(url)

    for node in cat_nodes:
        time.sleep(1)
        pull_node(get_url(node))

print master_nodes

with open('./browsenodesid.txt','a') as f:
    for ele in master_nodes:
        f.write(ele+',')




