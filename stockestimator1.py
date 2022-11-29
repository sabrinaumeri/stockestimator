import spacy
nlp = spacy.load("en_core_web_sm")

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
print(f.read())
f.close()

