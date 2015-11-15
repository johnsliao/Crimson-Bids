class iPhone:
    def __init__(self):
        self.att = ['ATT','AT&T','AT']
        self.verizon = ['VERIZON','VERIZONWIRELESS']
        self.sprint = ['SPRINT']
        self.tmobile = ['TMOBILE','T-MOBILE']
        self.unlocked = ['UNLOCKED']

        self.storage = ['4GB', '8GB', '16GB','32GB','64GB','128GB']

        self.model = ['4S', '4', '5C', '5S', '5', '6PLUS', '6']
        self.unsupported_models = ['1', '3', '3G']

        self.color = ['SILVER','BLACK','SLATE','WHITE','SPACE','GOLD','BLUE','WHITE',
                      'YELLOW','GREEN','PINK','CLEAR','SILVER','GRAY']

    def getCarrier(self, title):
        if any(word in title for word in self.att):
            return 'ATT'
        if any(word in title for word in self.verizon):
            return 'VERIZON'
        if any(word in title for word in self.sprint):
            return 'SPRINT'
        if any(word in title for word in self.tmobile):
            return 'TMOBILE'
        if any(word in title for word in self.unlocked):
            return 'UNLOCKED'

        return 'CARRIER-DNE'

    def getStorage(self, title):

        for word in title:
            for storage in self.storage:
                if word == storage:
                    return storage

        return 'STORAGE-DNE'

    def getModel(self, title):
        if 'PLUS' in title: # hacking 6plus to work...
            return '6PLUS'

        for word in title:
            for model in self.model:
                if word == model:
                    return model
            for model in self.unsupported_models:
                if word == model:
                    return "N/A"
        return 'MODEL-DNE'

    def getColor(self, title):
        for word in title:
            for color in self.color:
                if word == color:
                    return color
        return 'COLOR-DNE'


    def check_title_attributes(self, title):
        title = title.replace('/', ' ')
        title = title.replace("""'\'""", ' ')
        title = title.replace(',', ' ')
        title = title.replace('"', '')
        title = title.replace('-', '')
        title = title.replace('(', '')
        title = title.replace(')', '')
        title = title.replace('!', '')
        title = title.strip()
        title = title.upper()

        title = title.split()

        return [self.getCarrier(title), self.getStorage(title), self.getModel(title), self.getColor(title)]


def main():
    title = 'Apple iPhone 5C 16GB "Factory Unlocked" 4G LTE Smartphone'

    c = iPhone()
    print c.check_title_attributes(title)



if __name__ == '__main__':
    main()