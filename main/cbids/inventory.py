import datetime
from collections import defaultdict

class Inventory:
    def __init__(self):
        self.product_list = []
        self.inventory = defaultdict(int)
        
    def add_inventory(self, product_id):
        self.inventory[product_id] += 1

    def export_inventory(self):
        current_date = 'D'+datetime.date.today().strftime("%B%d%Y")
        current_time = 'T'+datetime.datetime.now().strftime("%I%M")
        fname = r'C:/Temp/Inventory-'+current_date+'.'+current_time+'.txt'
        
        with open(fname, 'w') as fs:
            for entry in self.inventory:
                fs.write(entry)
                fs.write(' ')
                fs.write(entry[1])
                fs.write('\n')

    def import_product_list(self, fname):
        with open(fname, 'r') as fs:
            for line in fs:
                carrier, storage, model, color, productid = line.split()
                self.product_list.append((carrier, storage, model, color, productid))

    def retrieve_productid(self, attributes):
        for product in self.product_list:
            if product[0] == attributes[0] and product[1] == attributes[1] and product[2] == attributes[2] and product[3] == attributes[3]:
                return product[4]
        return (-1)   
