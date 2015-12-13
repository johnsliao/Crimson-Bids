# Crimson Bids

eBay listing scraper written in Python. Updates the listings every 10 minutes.

<a href="https://gyazo.com/49dc97d3d9e4ac3fc4a2bdf1e2905eff"><img src="https://i.gyazo.com/49dc97d3d9e4ac3fc4a2bdf1e2905eff.gif" alt="https://gyazo.com/49dc97d3d9e4ac3fc4a2bdf1e2905eff"/></a>

Some Key features
- performs language processing each product seller descriptions listing (keywords like "cracked", "scratched", "bad IMEID". Also negations taken into account)
- screens out poorly rated sellers (listings with sellers below 95% threshold are ignored)

Back end:
- XML/JSON navigation, Python libraries (lxml, json, requests, etc), cron, eBay API
- Hosted on Amazon EC2, uses Amazon tools such as DynamoDB to store/update the listings.

Front end:
- Bootstrap, JQuery/JavaScript, JQGrid, CSS, HTML, AJAX, 
