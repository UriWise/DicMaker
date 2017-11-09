#!/usr/bin/python
import sys, datetime, os

def getPrefixes():
    return ['!','@','#','$','%','*']
def getSuffixes():
    return ["1",'!','@','#','$',"?","123","1234","12345","123456","!@#","!!!",'1!',"!1","qaz","!!","321","$$$","111","666","777"]
def getInfixes():
    return ['-','&','!','@','#','$','2','4','?',"and","And","n","vs"]
def getNumDict():
    return {"a": ["@", "4"], "e": "3", "o": "0", "s": "$", "i": "1"}

def genYYYY(startYYYY,endYYYY):
    lstYYYY = []
    for y in range(startYYYY,endYYYY+1):
        lstYYYY.append(str(y))
    return lstYYYY

def genYY(startYYYY,endYYYY):
    lstYY = []
    for yy in range(startYYYY,endYYYY+1):
        lstYY.append(datetime.datetime.strptime(str(yy)+".01.01" ,'%Y.%m.%d').strftime('%y'))   
    return lstYY

def genDDMM():
    lstDDMM = []
    for j in range(1,367):
        lstDDMM.append(datetime.datetime.strptime("2016."+str(j), '%Y.%j').strftime('%d%m'))
    return lstDDMM
def genMMDD():
    lstMMDD = []
    for j in range(1,367):
        lstMMDD.append(datetime.datetime.strptime("2016."+str(j), '%Y.%j').strftime('%m%d'))
    return lstMMDD

def getWordlist(strFilename):
    lstWordlist = []
    wl = open(strFilename,'r')
    for line in wl:
        line = line.strip('\n')
        line = line.strip(' ')
        if (len(line)>0) and (line[:1]!="#"):
            lstWordlist.append(line)
    wl.close    
    return lstWordlist

def enrichCase(lstWordlist):
    lstEnriched = []
    for item in lstWordlist:
        lstEnriched.append(item)
        lstEnriched.append(item.title())
        lstEnriched.append(item.upper())
    return lstEnriched



def enrichInfixes(word1,word2):
    infixes = getInfixes()
    enriched = []
    for infix in infixes:
        enriched.append(word1+infix+word2)
    return enriched

         
def replaceChar(word,char_pos,ch):
    resWord = ""
    for c in range(0,len(word)):
        if c == char_pos:
            resWord += ch
        else:
            resWord += word[c]
    return resWord


def distinct(lst):
    newList = []
    for item in lst:
        if item not in newList:
            newList.append(item)
    return newList

def numerizeWord(word):
    lstNumerized = []
    dicSubs = getNumDict()
    for l in range(0,len(word)):
        if dicSubs.has_key(word[l].lower()):
            if type(dicSubs[word[l].lower()]) is list:
                for i in dicSubs[word[l].lower()]:
                    newWord = replaceChar(word, l, i)
                    lstNumerized.append(newWord)
                    lstNumerized+=numerizeWord(newWord)
            else:
                newWord = replaceChar(word,l,dicSubs[word[l].lower()])
                lstNumerized.append(newWord)
                lstNumerized+=numerizeWord(newWord)
    return distinct(lstNumerized)

######################################################################################################################
original_wordlist = getWordlist('wordlist.txt')
case_enriched_wordlist = enrichCase(original_wordlist)

yy = genYY(1970,2017)
# case_enriched_wordlist_with_YY = []
# for item in case_enriched_wordlist:
#     for year in yy:
#          case_enriched_wordlist_with_YY.append(item+year)
# 
yyyy = genYYYY(1970,2017)
# case_enriched_wordlist_with_YYYY = []
# for item in case_enriched_wordlist:
#     for year in yyyy:
#          case_enriched_wordlist_with_YYYY.append(item+year)
ddmm = genDDMM()

wordlist = []
outfile_name = "dictionary.txt"
suffixes = getSuffixes()

dates =yyyy
dates += yy
dates += ddmm

case_enriched_wordlist_with_suffixes = []
for word in case_enriched_wordlist:
    for suffix in suffixes:
        case_enriched_wordlist_with_suffixes.append(word+suffix)

case_enriched_wordlist_with_dates = []
for word in case_enriched_wordlist:
    for d in dates:
        case_enriched_wordlist_with_dates.append(word+d)

case_enriched_wordlist_with_dates_and_suffixes = []
for word in case_enriched_wordlist_with_dates:
    for suffix in suffixes:
        case_enriched_wordlist_with_dates_and_suffixes.append(word+suffix)
        
#### concatenate words ###
concatenates = []
for firstWord in case_enriched_wordlist:
    for secondWord in case_enriched_wordlist:
        if (firstWord.lower() != secondWord.lower()):
            concatenates.append(firstWord + secondWord)
            concatenates += enrichInfixes(firstWord,secondWord)

concatenates_with_suffixes = []
for item in concatenates:
    for suffix in suffixes:
        concatenates_with_suffixes.append(item+suffix)


wordlist += case_enriched_wordlist
wordlist += case_enriched_wordlist_with_suffixes
wordlist += case_enriched_wordlist_with_dates # dates as suffix
wordlist += case_enriched_wordlist_with_dates_and_suffixes
wordlist += concatenates
wordlist += concatenates_with_suffixes

numerized_wordlist = []
for item in wordlist:
    numerized_wordlist += numerizeWord(item)

wordlist += numerized_wordlist
print wordlist
print "Creating dictionary with " + str(len(wordlist)) + " words."


### Write wordlist to file ###
forWPA = True # WPA comaptible passwords only
file_line_count = 0
if (os.path.isfile(outfile_name)):
    os.remove(outfile_name)
    
outfile = open(outfile_name,'a')

for item in wordlist:
    if (forWPA == False or len(item)>7):
        outfile.write(item+'\n')
        file_line_count +=1
outfile.close()
print str(file_line_count) + " lines added to " + outfile_name

