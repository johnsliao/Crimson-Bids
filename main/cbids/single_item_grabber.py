from lxml import etree
from construct_url import Construct_URL

import requests
import cgi

class singleItem:

    def __init__(self, url, itemId):
        self.url = url

        self.itemId = itemId
        self.title = 'Not Available'
        self.description = 'Not Available'
        self.galleryURL = 'Not Available'
        self.sellerId = 'Not Available'
        self.sellerFeedbackScore = 'Not Available'
        self.sellerPositiveFeedbackPercent = 'Not Available'
        self.bidCount = 'Not Available'
        self.currentPrice = 'Not Available'
        self.shippingCostPaidBy = 'Not Available'
        self.paymentMethods = 'Not Available'
        self.returnPolicyDescription = 'Not Available'
        self.returnsAccepted = 'Not Available'
        self.pictureURLArray = []

    def parse(self):
        xml_obj = requests.get(self.url)

        xml = xml_obj.text

        formatted_xml = xml.replace('<?xml version="1.0" encoding="UTF-8"?>','')
        formatted_xml = formatted_xml.replace(' xmlns="urn:ebay:apis:eBLBaseComponents"', '')
        formatted_xml = formatted_xml.strip()
        formatted_xml = formatted_xml.encode('utf-8')

        root = etree.fromstring(formatted_xml)

        item = root.find('Item')

        if item.find('Description') is not None:
            self.description = item.find('Description').text.encode('utf8')

        self.title = item.find('Title').text

        if item.find('GalleryURL') is not None:
            self.galleryURL = item.find('GalleryURL').text

        self.sellerId = item.find('Seller').find('UserID').text
        self.sellerFeedbackScore = item.find('Seller').find('FeedbackScore').text
        self.sellerPositiveFeedbackPercent = item.find('Seller').find('PositiveFeedbackPercent').text

        self.bidCount = item.find('BidCount').text

        self.currentPrice = item.find('ConvertedCurrentPrice').text

        if item.find('PaymentMethods') is not None:
            self.paymentMethods = item.find('PaymentMethods').text

        if item.find('ReturnPolicy').find('Description') is not None:
            self.returnPolicyDescription = item.find('ReturnPolicy').find('Description').text

        if item.find('ReturnPolicy').find('ShippingCostPaidBy') is not None:
           self.shippingCostPaidBy = item.find('ReturnPolicy').find('ShippingCostPaidBy').text

        if item.find('ReturnPolicy').find('ReturnsAccepted') is not None:
            self.returnsAccepted = item.find('ReturnPolicy').find('ReturnsAccepted').text

        pictureURLobj = item.findall('PictureURL')

        for count, pictureURL in enumerate(pictureURLobj):
            if pictureURL is None:
                continue
            if count >2:
                continue

            url = pictureURL.text

            self.pictureURLArray.append(url)



def main():

    #form = cgi.FieldStorage()
    #itemId = form["itemId"].value
    #timeLeft = form[""]

    itemId = '141591888446'

    u = Construct_URL()
    url = u.single_product(itemId)
    print url

    i = singleItem(url, itemId)

    i.parse()


    print '''<html>
    <head><link href="../Bootstrap/css/bootstrap.min.css" rel="stylesheet">
    <link href="../Bootstrap/css/bootstrap-theme.min.css" rel="stylesheet">
    <link href="theme.css" rel="stylesheet">

    <script src="../jquery.js"></script>

    <link rel="stylesheet" href="../jqueryUI/jquery-ui.css">
    <script src="../jqueryUI/jquery-ui.js"></script>

    <style>
        .morecontent span {
            display: none;
        }
    </style>

    </head>
	<body>

    <div style="position: relative; left: 71%; top:115px">
        <a href="../about.html"> About</a> /
        <a href="../faq.html"> FAQ </a> /
        <a href="../feedback.html"> Send us your feedback </a>
    </div>

    <div class="container">
      <div class="page-header">
          <a href="../index.html"><img src="../logo.jpg" ><br></a>
        <h4>Quality Product Listings</h4></div>


        <h3><a target="_blank" href="http://rover.ebay.com/rover/1/711-53200-19255-0/1?icep_ff3=2&pub=5575124864&toolid=10001&campid=5337694064&customid=&icep_item='''+i.itemId+'''&ipn=psmain&icep_vectorid=229466&kwid=902099&mtid=824&kw=lg">'''+i.title+'''</a></h3>
        <p>
        '''+ ''.join(map('<a href="{}"><img src="{}" class="img-thumbnail" alt="listing snapshot" style="width:200px"></a>'.format, i.pictureURLArray, i.pictureURLArray))+'''
        </p>

        <div style="width:400px">
        <p><b>Item ID</b>: '''+i.itemId+'''</p>
        <b><p>Description</b></p>
        <div class="comment more">
        </p>'''+i.description+'''</p>
        </div><br>
        <p><b>Current price (USD)</b>: $'''+i.currentPrice+'''</p>
        <p><b>Bids</b>: '''+i.bidCount+'''</p><br>

        <p><b>Seller Info</b></p>
        <p>Seller: '''+i.sellerId+'''</p>
        <p>Feedback Score: '''+i.sellerFeedbackScore+'''</p>
        <p>Positive Feedback %: '''+i.sellerPositiveFeedbackPercent+'''</p><br>

        <p><b>Shipping Info</b></p>
        <p>Shipping cost paid by: '''+i.shippingCostPaidBy+'''</p><br>

        <p><b>Payment Info</b></p>
        <p>Accepted payment methods: '''+i.paymentMethods+'''</p>

        <br><br>
        <div class="panel panel-default" >
            <div class="panel-body">
        <p><b>Place bid</b></p>

        <p>This feature is coming soon! Thank you for your patience.</p>

        <!--
        <form action="./cgi-bin/#" method="get">

        $ (USD): <br>
        <input type="text" name="name">
        <input type="submit" value="Place Bid">

        </form> -->
	</form>
            </div>
        </div>

    <script>
            $(document).ready(function() {
            var showChar = 100;
            var ellipsestext = "...";
            var moretext = "more";
            var lesstext = "less";
            $('.more').each(function() {
                var content = $(this).html();

                if(content.length > showChar) {

                    var c = content.substr(0, showChar);
                    var h = content.substr(showChar-1, content.length - showChar);

                    var html = c + '<span class="moreelipses">'+ellipsestext+'</span>&nbsp;<span class="morecontent"><span>' + h + '</span>&nbsp;&nbsp;<a href="" class="morelink">'+moretext+'</a></span>';

                    $(this).html(html);
                }

            });

            $(".morelink").click(function(){
                if($(this).hasClass("less")) {
                    $(this).removeClass("less");
                    $(this).html(moretext);
                } else {
                    $(this).addClass("less");
                    $(this).html(lesstext);
                }
                $(this).parent().prev().toggle();
                $(this).prev().toggle();
                return false;
            });
        });
    </script>

    <script>
        (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
        (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
        m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
        })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

        ga('create', 'UA-62663706-1', 'auto');
        ga('send', 'pageview');
    </script>
	</body>
</html>'''


if __name__ == '__main__':
    main()