# Crimson Bids

Built a eBay listing scraper written in Python. Updates the listings every 10 minutes.

Some Key features
- performs language processing each product seller descriptions listing (keywords like "cracked", "scratched", "bad IMEID". Also negations taken into account)
- screens out poorly rated sellers (listings with sellers below 95% threshold are ignored)

Back end:
- XML/JSON navigation, Python libraries (lxml, json, requests, etc), cron, eBay API
- Hosted on Amazon EC2, uses Amazon tools such as DynamoDB to store/update the listings.

Front end:
- Bootstrap, JQGrid, CSS, HTML, AJAX
