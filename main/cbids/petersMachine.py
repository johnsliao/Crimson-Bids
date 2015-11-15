import re

TEXT = ''

#with open('./TEXT.txt','r') as f:
#    for line in f:
#        TEXT += line


class IPhoneVault:
    
    def __init__(self):
        self.physicalCondition = 'UNDEFINED'
        self.accessories = {}
        self.IMEI = 'UNDEFINED'
        self.ESN = 'UNDEFINED'
        self.iCloud = 'UNDEFINED'
        self.functionalityCondition = {}

    def setPhysicalCondition(self, physicalCondition):
        self.physicalCondition = physicalCondition

    def setAccessories(self, accessories):
        self.accessories.update(accessories)

    def setIMEI(self, status):
        self.IMEI = status

    def setESN(self, status):
        self.ESN = status

    def setICloud(self, status):
        self.iCloud = status

    def setFunctionalityCondition(self, status):
        self.functionalityCondition.update({'Functionality' : status})

    def getStatus(self):
        print '* * * RESULTS * * *'
        print 'Physical condition:', self.physicalCondition
        print 'Accessories:', self.accessories
        print 'IMEI status:', self.IMEI
        print 'ESN status:', self.ESN
        print 'iCloud status:', self.iCloud
        print 'Functionality status', self.functionalityCondition
        print '\n'
        

        if 'LOCKED' == self.IMEI or 'LOCKED' == self.ESN or 'LOCKED' == self.iCloud:
            print 'Viable Product Decision: REJECT'
            return False

        if 'BAD' in self.functionalityCondition.values():
            print 'Viable Product Decision: REJECT'
            return False

        if self.physicalCondition == 'GOOD':
            print 'Viable Product Decision: ACCEPT'
            return True
        
        print 'Viable Product Decision: REJECT'
        return False
        
class Dictionary:

    def __init__(self, inputText):
        self.IPhoneDictionary = IPhoneDictionary()
        self.inputText = inputText

    def pushThroughIphoneMachine(self):
        self.IPhoneDictionary.interpretText(self.inputText)

class IPhoneDictionary:

    def __init__(self):
        self.IPhoneGoodConditions = IPhoneGoodConditions() # physical conditions
        self.IPhoneBadConditions = IPhoneBadConditions() # physical conditions
        self.IPhoneComesWith = IPhoneComesWith()
        self.IPhoneIMEI = IPhoneIMEI()
        self.IPhoneICloud = IPhoneICloud()
        self.IPhoneESN = IPhoneESN()
        self.IPhoneFunctionalityConditions = IPhoneFunctionalityConditions()
        
        self.IPhoneReasonsToSell = IPhoneReasonsToSell()
        self.IPhoneWarranty = IPhoneWarranty()

        self.IPhoneVault = IPhoneVault()
        
        self.onDeck = {}

    def iPhoneVaultStatus(self):
        self.IPhoneVault.getStatus();

    def addOnDeck(self, key, value):
        self.onDeck[key] = value

    def interpretOnDeck(self):
        if 'badConditionStatus'in self.onDeck and 'goodConditionStatus' in self.onDeck:
            self.IPhoneVault.setPhysicalCondition('???')
            
        elif 'badConditionStatus' in self.onDeck:
            self.IPhoneVault.setPhysicalCondition('BAD')
            
        elif 'goodConditionStatus' in self.onDeck:
            self.IPhoneVault.setPhysicalCondition('GOOD')

        self.IPhoneVault.setAccessories(self.IPhoneComesWith.getAccessories())
        self.IPhoneVault.setIMEI(self.IPhoneIMEI.getStatus())
        self.IPhoneVault.setESN(self.IPhoneESN.getStatus())
        self.IPhoneVault.setICloud(self.IPhoneICloud.getStatus())
        self.IPhoneVault.setFunctionalityCondition(self.IPhoneFunctionalityConditions.getStatus())
               

    def interpretText(self, inputText): # run text through conditionalClasses
        sentences = splitParagraphIntoSentences(inputText)

        for sentence in sentences:
            if len(sentence) == 0: # fix later
                continue

            print '-------------------------------------------------------------------'
            print 'Currently onDeckDict: ', self.onDeck

            sentence = sentence.strip()

            print 'Currently inspecting sentence: ', sentence

            sentence = sentence.split()

            self.IPhoneBadConditions.push(sentence)
            self.IPhoneGoodConditions.push(sentence)
            self.IPhoneComesWith.push(sentence)
            self.IPhoneIMEI.push(sentence)
            self.IPhoneESN.push(sentence)
            self.IPhoneICloud.push(sentence)
            self.IPhoneFunctionalityConditions.push(sentence)
            
            if self.IPhoneBadConditions.getStatus() == 'SATURATED':
                print 'Identified Sentence in Bad Subdict'
                self.addOnDeck('badConditionStatus', 'SATURATED')

            if self.IPhoneBadConditions.getStatus() == 'NEGATION':
                print 'Identified Sentence in Bad Subdict but Negated!'
                self.addOnDeck('goodConditionStatus', 'NEGATION')

            if self.IPhoneGoodConditions.getStatus() == 'SATURATED':
                print 'Identified Sentence in Good '
                self.addOnDeck('goodConditionStatus', 'SATURATED')

            if self.IPhoneGoodConditions.getStatus() == 'UNSATURATED' and self.IPhoneBadConditions.getStatus() == 'UNSATURATED':
                print 'Could not identify condition in sentence'

            print '\nEnding statuses after interpret bloc:'
            print 'badCondition status:', self.IPhoneBadConditions.getStatus()
            print 'goodCondition status:', self.IPhoneGoodConditions.getStatus()

            self.IPhoneBadConditions.clear()
            self.IPhoneGoodConditions.clear()
    
        print '\n.\n.\n.\n.\n'
        print '-------------------------------------------------------------------'

        self.interpretOnDeck()
        
        self.iPhoneVaultStatus()

class IPhoneGoodConditions:
    # Contains the logic to discern Good IPhone physical qualities

        def __init__(self):
            self.keywords = [
                'mint',
                'perfect',
                'pristine',
                'great',
                'excellent',
                'immaculate'
            ]

            self.conditionalKeywords = [
                'new'
            ]

            self.status = 'UNSATURATED'

        def push(self, sentence):
            for word in sentence:
                word = word.replace(',','')

                for keyword in self.keywords:
                    if keyword == word:
                        print 'Matched: ', keyword
                        self.status = 'SATURATED'

                for keyword in self.conditionalKeywords:
                    if keyword == word and 'CONDITION' in sentence or 'BRAND' in sentence: # Special set of keywords for "new" condition/ brand "new"
                        print 'Conditional "new" match!'
                        self.status = 'SATURATED'

        def getStatus(self):
            return self.status

        def clear(self):
            self.status = 'UNSATURATED'

class IPhoneBadConditions:
    # Contains the logic to discern Bad IPhone physical qualities

        def __init__(self):
            self.keywords = [
                'crack',
                'cracked',
                'broke',
                'broken',
                'scratch',
                'scratches',
                'chip',
                'chips',
                'chipped',
                'dent',
                'dented',
                'scuff',
                'scuffed',
                'damage',
                'damaged',
                'broke',
                'broken',
                'stuck',
                'blacklisted'
            ]

            self.negations = [
                'no',
                'not',
                'free',
                'tiny',
                "doesn't",
                'does not',
                'jail',
                'never'
            ]

            self.status = 'UNSATURATED'


        def push(self, sentence):

            for wordPosition, word in enumerate(sentence):
                word = word.replace(',','')

                for keywordPosition, keyword in enumerate(self.keywords):
                    if keyword in word:
                        print 'Matched: ', keyword, 'at position', wordPosition

                        if self.hasNegation(sentence, wordPosition) and self.status != 'SATURATED': # keep bad condition if negation found...
                            print 'setnegation for ', keyword
                            self.status = 'NEGATION'
                        if not self.hasNegation(sentence, wordPosition):
                            self.status = 'SATURATED'

        def hasNegation(self, sentence, wordPosition): # counts backwards from word to find negation
            tempWordPosition = wordPosition

            for count in range(4): # go back 4 words
                if tempWordPosition < 0:
                    continue

                tempWordPosition -= 1

                if sentence[tempWordPosition] in self.negations:
                    return True
            return False

        def getStatus(self):
            return self.status

        def clear(self):
            self.status = 'UNSATURATED'

class IPhoneComesWith:
    # Contains the logic to discern IPhone "Comes With" attributes

    def __init__(self):
        self.accesories = { # {accessory:state}
            'CHARGER':'UNDEFINED',
            'BOX':'UNDEFINED',
            'PROTECTOR':'UNDEFINED', # screen
            'CASE':'UNDEFINED',
            'HEADPHONE':'UNDEFINED',
            'CABLE':'UNDEFINED',
            'MANUAL':'UNDEFINED'
        }

        self.negations = [
            'no',
            'tiny',
            "doesn't",
            'does not',
            'minus'
        ]

    def push(self, sentence):

        for wordPosition, word in enumerate(sentence):
            word = word.replace(',','')

            for accessory in self.accesories:

                if accessory in word and not self.hasNegation(sentence, wordPosition):
                    print 'Found accessory:', accessory
                    self.accesories[accessory] = 'YES'

    def getAccessories(self):
        return self.accesories


    def hasNegation(self, sentence, wordPosition): # counts backwards from word to find negation
        tempWordPosition = wordPosition

        for count in range(4): # go back 4 words
            if tempWordPosition < 0:
                continue

            tempWordPosition -= 1

            if sentence[tempWordPosition] in self.negations:
                return True
        return False

class IPhoneIMEI:
    def __init__(self):
        self.status = 'UNDEFINED'

        self.negations = [
            'no',
            'not'
        ]

    def push(self, sentence):

        for wordPosition, word in enumerate(sentence):
            word = word.replace(',','')

            if 'imei' in word:
                self.searchStatus(sentence, wordPosition)

    def searchStatus(self, sentence, wordPosition):
        print len(sentence)
        for count in range(-8,9): # check 8 words backwards and forwards
            
            tempWordPosition = wordPosition
            tempWordPosition += count

            if tempWordPosition > len(sentence)-1 or tempWordPosition < 0 or tempWordPosition == 0:
                continue
            
            if 'locked' in sentence[tempWordPosition] and not self.hasNegation(sentence, wordPosition):
                self.status = 'LOCKED'
            if 'locked' in sentence[tempWordPosition] and self.hasNegation(sentence, wordPosition):
                self.status = 'CLEAN'
            if 'clean' in sentence[tempWordPosition]:
                self.status = 'CLEAN'

    def getStatus(self):
        return self.status

    def hasNegation(self, sentence, wordPosition): # counts backwards from word to find negation
        tempWordPosition = wordPosition

        for count in range(4): # go back 4 words
            if tempWordPosition < 0:
                continue

            tempWordPosition -= 1

            if sentence[tempWordPosition] in self.negations:
                return True
        return False


class IPhoneESN:
    # Contains the logic to discern ESN locked or not qualities
    def __init__(self):
        self.status = 'UNDEFINED'

        self.negations = [
            'no',
            'not'
        ]

    def push(self, sentence):
        for wordPosition, word in enumerate(sentence):
            word = word.replace(',','')

            if 'esn' in word:
                self.searchStatus(sentence, wordPosition)

    def searchStatus(self, sentence, wordPosition): 

        for count in range(-8,9):

            tempWordPosition = wordPosition
            tempWordPosition += count

            if tempWordPosition > len(sentence)-1 or tempWordPosition < 0 or tempWordPosition == 0:
                continue
            
            if 'locked' in sentence[tempWordPosition] and not self.hasNegation(sentence, wordPosition):
                self.status = 'LOCKED'
            if 'bad' in sentence[tempWordPosition] and not self.hasNegation(sentence, wordPosition):
                self.status = 'LOCKED'
            if 'locked' in sentence[tempWordPosition] and self.hasNegation(sentence, wordPosition):
                self.status = 'CLEAN'
            if 'clean' in sentence[tempWordPosition]:
                self.status = 'CLEAN'

    def getStatus(self):
        return self.status

    def hasNegation(self, sentence, wordPosition): # counts backwards from word to find negation
        tempWordPosition = wordPosition

        for count in range(4): # go back 4 words
            if tempWordPosition < 0:
                continue

            tempWordPosition -= 1

            if sentence[tempWordPosition] in self.negations:
                return True
        return False

class IPhoneICloud:
    # Contains the logic to discern ICloud locked or not qualities
    def __init__(self):
        self.status = 'UNDEFINED'
        
        self.negations = [
            'no',
            'not'
        ]

    def push(self, sentence):
        for wordPosition, word in enumerate(sentence):
            word = word.replace(',','')

            if 'CLOUD' in word:
                self.searchStatus(sentence, wordPosition)

    def searchStatus(self, sentence, wordPosition): # check 3 words backwards and forwards

        for count in range(-8,9):

            tempWordPosition = wordPosition
            tempWordPosition += count

            if tempWordPosition > len(sentence)-1 or tempWordPosition < 0 or tempWordPosition == 0:
                continue

            if 'LOCKED' in sentence[tempWordPosition] and not self.hasNegation(sentence, wordPosition):
                self.status = 'LOCKED'
            if 'LOCKED' in sentence[tempWordPosition] and self.hasNegation(sentence, wordPosition):
                self.status = 'CLEAN'
            if 'CLEAN' in sentence[tempWordPosition]:
                self.status = 'CLEAN'

    def getStatus(self):
        return self.status

    def hasNegation(self, sentence, wordPosition): # counts backwards from word to find negation
        tempWordPosition = wordPosition

        for count in range(4): # go back 4 words
            if tempWordPosition < 0:
                continue

            tempWordPosition -= 1

            if sentence[tempWordPosition] in self.negations:
                return True
        return False

class IPhoneFunctionalityConditions:
    # Handles the operability of the product
    
    def __init__(self):
            self.keywords = [
                'operable',
                'functional'
            ]

            self.negations = [
                'no',
                'not',
                'except'
            ]

            self.status = 'UNDEFINED'

    def push(self, sentence):
        for wordPosition, word in enumerate(sentence):
            word = word.replace(',','')

            if word == 'CAMERA' and self.hasOperabilityKeyword(sentence, wordPosition):
                print 'Camera Keyword Found'
                print 'Matched: CAMERA at position', wordPosition
                
                if self.hasNegation(sentence, wordPosition) is True:
                    print 'CAMERA IS BAD'
                    self.status = 'BAD'
                    
                if self.hasNegation(sentence, wordPosition) is not True and self.status != 'BAD':
                    print 'CAMERA IS GOOD'
                    self.status = 'GOOD'

    def hasOperabilityKeyword(self, sentence, wordPosition): # counts backwards from word to find negation
        tempWordPosition = wordPosition

        for count in range(-5,6):
            tempWordPosition = wordPosition
            tempWordPosition += count

            if tempWordPosition > len(sentence)-1 or tempWordPosition < 0 or tempWordPosition == 0:
                continue
            
            print sentence[tempWordPosition]
            
            tempWordPosition -= 1

            if sentence[tempWordPosition] in self.keywords:
                return True
            
        return False


    def hasNegation(self, sentence, wordPosition): # counts backwards from word to find negation
        tempWordPosition = wordPosition

        for count in range(4): # go back 4 words
            if tempWordPosition < 0:
                continue

            tempWordPosition -= 1

            if sentence[tempWordPosition] in self.negations:
                return True
            
        return False

    def getStatus(self):
        return self.status

class IPhoneReasonsToSell:
    # Contains the logic to discern why user wants to sell
    pass

class IPhoneWarranty:
    # Contains the logic to discern Warranty and time left + Apple Care
    pass

def splitParagraphIntoSentences(paragraph):
    sentenceEnders = re.compile('[.!?:]')
    sentenceList = sentenceEnders.split(paragraph)

    return sentenceList

def main():
    print 'DESCRIPTION INPUT: ', TEXT.lower(), '\n'

    dictionary = Dictionary(TEXT.lower()) # Change input here!
    dictionary.pushThroughIphoneMachine()

if __name__ == "__main__":
    main()
