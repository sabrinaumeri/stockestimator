import spacy
nlp = spacy.load("en_core_web_sm")
denomination = {'hundred': '00','thousand': '000','million': '000000','billion': '000000000' }
# Read data from text file


# Operation #1 - Do an initial parse on the emails log file and extract the POS and entity tags for each of the emails. This information should be stored in a separate text file
inputfile = open('EmailLog.txt', mode='r', encoding='utf-8')
outputfile = open ('ParsedFile.txt', mode='wt', encoding='utf-8')

p = inputfile.read()
doc = nlp(p)

for token in doc:
    outputfile.write(token.text + "," + token.pos_ + "," + token.tag_ + "," + token.dep_ + "," + str(spacy.explain(token.dep_)) + '\n')
    
inputfile.close()
outputfile.close()

# read spaCy data from a text file
f = open('ParsedFile.txt', mode='r', encoding='utf-8')

f.close()


# Operation #2  - The generated stored text file which in step 1 can subsequently be consumed(optional) by another python script to get the proper output in the console. 
# Or you canuse entirely spaCy script to handle all the required tasks without using the generated text file from step 1.
f = open('EmailLog.txt', mode='r', encoding='utf-8')
print('Stock Buy/Sell Estimator -  Sabrina Umeri, Devon Tully, Manh Cuong Nguyen\n')
printToConsole = ""
request = ""
email = ''
grandTotal = 0
for line in f:
  totalInvested = 0
  line = line.strip('\n')
  if(line == "<<End>>"):
      email = ''
      request = ''
      totalstring = ''
  doc = nlp(line)
  companies = []
  dollarAmounts = []
  for token in doc:
        if(token.like_email):
              email += token.text + " : "
        elif token.tag_ == '$':
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
                print (email+ request + formattedString + '.\n')
              else:
                print(email + request + '\n')  
        
            
printToConsole += "Total Requests: ${:0,.2f}".format(grandTotal)
f.close()


print (printToConsole)