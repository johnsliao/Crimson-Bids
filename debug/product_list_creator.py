carriers = ['ATT','VERIZON', 'SPRINT','TMOBILE','UNLOCKED']
_4_storages = ['8GB', '16GB','32GB']
_4S_storages = ['8GB', '16GB','32GB', '64GB']
_5_storages = ['16GB','32GB','64GB']
_5c_storages = ['8GB', '16GB','32GB']
_5S_storages = ['16GB','32GB','64GB']
_6_storages = ['16GB','64GB','128GB']

models = ['4S', '4', '5C', '5S', '5', '6PLUS', '6']

_4_colors = ['BLACK','WHITE']
_4S_colors = ['BLACK','WHITE']
_5_colors = ['BLACK', 'SLATE','WHITE','PINK','YELLOW','BLUE','RED','GRAY']
_5c_colors = ['WHITE','PINK','YELLOW','BLUE','GREEN']
_5S_colors = ['SILVER','SPACE','GOLD','GRAY']
_6_colors = ['SILVER','SPACE','GOLD','GRAY']

productid=1

with open(r'product_list.txt', 'w') as fs:
#with open(r'C:\Users\usjli\Dropbox\coding\product_list.txt', 'w') as fs:
    entry= 'carrier storage model color productid'
    fs.write(entry)
    entry = '\n'
    
    for carrier in carriers:
            for model in models:
                if model == '4':
                    for _4_color in _4_colors:
                        for _4_storage in _4_storages:
                            entry += carrier+ ' '+_4_storage+ ' '+model+ ' '+_4_color + ' ' +str(productid)+'\n'
                            fs.write(entry)
                            productid += 1
                            entry= ''

                if model == '4S':
                    for _4S_color in _4S_colors:
                        for _4S_storage in _4S_storages:
                            entry += carrier+ ' '+_4S_storage+ ' '+model+ ' '+_4S_color + ' ' +str(productid)+'\n'
                            fs.write(entry)
                            productid += 1
                            entry= ''

                if model == '5':
                    for _5_color in _5_colors:
                        for _5_storage in _5_storages:
                            entry += carrier+ ' '+_5_storage+ ' '+model+ ' '+_5_color + ' ' +str(productid)+'\n'
                            fs.write(entry)
                            productid += 1
                            entry= ''

                if model == '5C':
                    for _5c_color in _5c_colors:
                        for _5c_storage in _5c_storages:
                            entry += carrier+ ' '+_5c_storage+ ' '+model+ ' '+_5c_color +' ' +str(productid)+'\n'
                            fs.write(entry)
                            productid += 1
                            entry= ''

                if model == '5S':
                    for _5S_color in _5S_colors:
                        for _5S_storage in _5S_storages:
                            entry += carrier+ ' '+_5S_storage+ ' '+model+ ' '+_5S_color +' ' +str(productid)+'\n'
                            fs.write(entry)
                            productid += 1
                            entry= ''

                if model == '6' or model == '6PLUS':
                    for _6_color in _6_colors:
                        for _6_storage in _6_storages:
                            entry += carrier+ ' '+_6_storage+ ' '+model+ ' '+_6_color +' ' +str(productid)+'\n'
                            fs.write(entry)
                            productid += 1
                            entry= ''
