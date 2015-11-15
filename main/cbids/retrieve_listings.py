import requests
from lxml import html
screenout_keywords = ['BAD', 'POOR', 'CRACKED', 'CRACKS', 'BROKEN','SCRATCH', 'SCRATCHES','CHIPPED', 'CHIPS', 'CHIP', 'DENT', 'DENTS', 'SCUFF', 'SCUFFING', 'SCRATCHING']

url = 'http://www.ebay.com/itm/Apple-iPhone-4s-32GB-Black-Sprint-Smartphone-with-Extras-Great-Condition-/151622961206?pt=LH_DefaultDomain_0&nma=true&si=eNGAJ0XOqaZdTCTtiHf%252BdN2%252BYu0%253D&orig_cvip=true&rt=nc&_trksid=p2047675.l2557'

page = requests.get(url)
tree = html.fromstring(page.text)

sellerNotes = tree.xpath('//span[@class="viSNotesCnt"]/text()')

print sellerNotes
sellerNotes = sellerNotes
print sellerNotes[0]

for word in sellerNotes:
    for screenout_keyword in screenout_keywords:
        if screenout_keyword in word.upper() :
            print 'Reject! SellerNotes screenout keyword activated:', word