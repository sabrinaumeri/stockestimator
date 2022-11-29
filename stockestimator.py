import spacy
nlp = spacy.load("en_core_web_sm")
denomination = {'thousand': '000' }
# Read data from text file
f = open('EmailLog.txt', mode='r', encoding='utf-8')

print('Stock Buy/Sell Estimator -  Sabrina Umeri, Devon Tully, Manh Cuong Nguyen\n')
printToConsole = ""
request = ""
email = ''
grandTotal = 0
for line in f:
    totalInvested = 0
    line = line.strip('\n')
    match line:
        case "<<End>>":
              email = ''
              request = ''
        case _:
            doc = nlp(line)
            companies = []
            dollarAmounts = []
            for token in doc:
                if(token.like_email):
                    email += token.text + " : "
                    break
                if token.tag_ == '$':
                    numInvested = ''
                    i = token.i + 1
                    while doc[i].tag_ == 'CD':
                        if doc[i].text in denomination:
                            numInvested += denomination[doc[i].text]
                        else:
                            numInvested += doc[i].text
                        i += 1
                    totalInvested += int(numInvested.replace(',', ''))
                    grandTotal += int(numInvested.replace(',', ''))
                    dollarAmounts.append(int(numInvested.replace(',', ''))) 
                elif (token.dep_ == 'pobj' and token.tag_ != 'CD'):
                     i = token.i-1
                     companyName = ''
                     if doc[i].dep_ == 'compound':
                       companyName = doc[i].text
                     else:
                       companyName = token.text
                     companies.append(companyName)                
    if totalInvested > 0:
        request = ''
        request += "${:,.0f}".format(totalInvested)+' to '
        if(len(companies) > 1):
            for i in range(len(companies)):
              if (len(companies) == 2):
                    request += companies[i] + ' and ' + companies[i+1] + '.'
                    break
              elif i == len(companies)-1:
                request += 'and '
                request += companies[i] + '.'
                break
              else :
                request += companies[i] + ', '
        else:
          request += companies[0] + '.'
        if (email != ''):
          if len(companies) > 1:
            formattedString = ''
            for i in range(len(companies)):
              if (i < len(companies)-1):            
                formattedString +=  " ${:,.0f}".format(dollarAmounts[i]) + ' to ' + companies[i] + ','
              else:
                formattedString += ' and ' + "${:,.0f}".format(dollarAmounts[i]) + ' to ' + companies[i] 
            printToConsole += (email+ request + formattedString + '.\n')
          else:
            printToConsole +=(email + request + '\n')  
          printToConsole += "\n"  
        


printToConsole +=("Total Requests: ${:0,.2f}".format(grandTotal))

print (printToConsole)
f.close()