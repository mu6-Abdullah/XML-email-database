import itertools
import sys
 
def main():
    try:
        file = sys.argv[1]
        contents = readFile(file)#file input
    except IndexError:
        print("No XML file provided!")
        return
    except OSError:
        print("The File is not in the neighbourhood.")
        return
 
    contents.pop(0) #pop the first 2 elements
    contents.pop(0) 
    contents.pop(len(contents)-1) #pop the last element
    pList = partitionFile(contents) #partition the file
    #create a list for each output file going to put out
    tList = createTerms(pList)
    dList = createDates(pList)
    eList = createEmails(pList)
    rList = createRecs(pList)
    #write out each file
    writeTerms(tList)
    writeDates(dList)
    writeEmails(eList)
    writeRecs(rList)
 
def readFile(file_name):
    file = open(file_name,"r")
    contents = []# a list of all the entries
    for line in file:
        term = line.split('\n') #split upon the newline character
        term = term[0]#removes any empty spaces
        contents.append(term) 
    file.close()
    return contents
 
def partitionFile(contents):
    outputList =[] #create an output list
    for entry in contents: #for each entry
        entry = entry.split('<')  #split upon < character
        entryList= []
        for element in entry:
            if element != '': #if element is nonempty  
                element = element.split('>') #split again upon the > character
                element[0] = '<'+element[0]+'>' #since the < and > have been removed, but the file properly split, add the chracters back
                if element[1] == '':
                    element.pop(1) #if the second element of the list is empty pop it
                #The case ignoring was originally here
                for elements in element:
                    entryList.append(elements)
        outputList.append(entryList)
    return outputList
 
def createTerms(pList):
    terms = []
    for entry in pList: 
        row_id = entry[2] #get the row_id
        for element in entry:
            #print(element + " IS THE ELEMENT")
            #print(entry[entry.index(element)+1] + ' IS THE NEXT ELEMENT')
            if '<body>' == element: #if the body is found
                element = entry[entry.index(element) + 1] #the next element is the text of the body
                element = element.lower() #conver to tlowercase
                field = 'b'
                words = element.split(' ')#split all the words at any whitespace
                for word in words:
                    #print(word)
                    word = word.replace('&lt;','<')
                    word = word.replace('&gt;','>')
                    word = word.replace('&amp;','&')
                    word = word.replace('&apos;',"'")
                    word = word.replace('&quot;','"')
                    word = word.replace('&#10;',' ')
                    word = word.replace('?','')
                    word = word.strip('.') #strip the words of any attached periods and commas
                    word = word.strip(',')
                    #print(word.count('-'))
                    if ' ' in word:
                        words = word.split()
                        for word in words:
                            #print(word)
                            if word == '' or word == ' ':
                                words.pop(words.index(word))
                            word = word.strip('.') #strip the words of any attached periods and commas
                            word = word.strip(',')
                            word = word.replace('?','') #check if the first and last characters are alphanumeric, and if there is only one hyphen
                            if len(word)>2 and word.isalnum() :
                                terms.append([field,word,row_id])
                            elif '-' in word and len(word) > 2:
                                terms.append([field,word,row_id])
                    elif len(word) > 2 and word.isalnum(): #if the word is greater than 2 characters and is only characters
                        terms.append([field,word,row_id])
                    elif '-' in word and len(word) > 2:
                        terms.append([field,word,row_id]) #add it to terms
                    elif '/' in word and len(word) > 2:
                        #print(word)##################HERE
                        word = word.split('/')
                        for each in word:
                            #print("Body:",each)
                            terms.append([field,each,row_id])
 
            elif '<subj>' == element and '</subj>' != entry[entry.index(element)+1] : #if the subj start tag is found, adn the next element is not the end tag
                element = entry[entry.index(element) + 1] # the next element is the text of subject
                element= element.lower() # convert to lowercase
                field = 's'
                words = element.split() # split on whitespace
                for word in words:
                    word = word.replace('&lt;','<')
                    word = word.replace('&gt;','>')
                    word = word.replace('&amp;','&')
                    word = word.replace('&apos;',"'")
                    word = word.replace('&quot;','"')
                    word = word.replace('&#10;',' ')
                    #word = word.replace('/',' ')
                    word = word.strip('.') #strip the words of any attached periods and commas
                    word = word.strip(',')
                    #print(word)
                    if ' ' in word:
                        words = word.split()
                        for word in words:
                            if word == '' or word == ' ' :
                                words.pop(words.index(word))
                            word = word.strip('.') #strip the words of any attached periods and commas
                            word = word.strip(',')
                            if len(word)>2 and word.isalnum():
                                terms.append([field,word,row_id])
                            elif '-' in word and len(word) > 2:
                                terms.append([field,word,row_id])
                    elif len(word) > 2 and word.isalnum():
                        terms.append([field,word,row_id])
                    elif '-' in word and len(word) > 2:
                        terms.append([field,word,row_id])
                    elif '/' in word and len(word) > 2:
                        word = word.split('/')
                        for each in word:
                            #print('subject:',each)##############HERE
                            terms.append([field,each,row_id])
    #for i in terms:
    #    print(i)
    return terms
 
def writeTerms(tList):
    f = open("terms.txt","w+") #write the terms file
    for i in range(len(tList)):
        f.write(tList[i][0]+'-'+tList[i][1]+':'+tList[i][2]+'\n')
    f.close()
 
def createDates(pList):
    #create Dates Dictionary
    #the rows will be the key, and the the dates will be the value
    dates = []
    for entry in pList:
        for element in entry:
            row_id=entry[2] #grab the row_id
            if '<date>' == element: #if the data start tag is found
                element = entry[entry.index(element)+1] # the next element is the date
                dates.append([element,row_id])
 
    return dates
 
def writeDates(dList): #write the dates.txt file
    f = open("dates.txt","w+")
    for i in range(len(dList)):
        f.write(dList[i][0]+':'+dList[i][1]+'\n')
    f.close()
 
def createEmails(pList):
    #create Emails list
    #for each entry find emails in these sections, to, from, cc,bcc
    #create a list of lists, the inner list will be [[rowid],[toemail],[fromemail],[bcc-email],[cc-email]]
    emails =[]
    for entry in pList:
        row_id=entry[2]
        for element in entry:
            #print(element)
            if '<from>' == element: #if from start tag
                next_element = entry[entry.index(element)+1]
                if next_element != "</from>":#make sure the next element is not the end tag
                    element = next_element.lower()
                    field = 'from'
                    emails.append([field,element,row_id])# append
            elif '<to>' == element:
                next_element = entry[entry.index(element)+1]
                if next_element != "</to>":#make sure the next element is not the end tag
                    field = 'to'
                    element = next_element.lower()
                    if ',' in element:
                        element = element.split(',')
                        for elements in element:
                            emails.append([field,elements,row_id])
                    else:
                        emails.append([field,element,row_id])#append
            elif'<cc>' == element: #next element is cc emails
                next_element = entry[entry.index(element)+1]
                if next_element != "</cc>":#make sure the next element is not the end tag
                    element = next_element.lower()
                    field = 'cc'
                    if ',' in element:
                        element = element.split(',')
                        for elements in element:
                            emails.append([field,elements,row_id])
                    else:
                        emails.append([field,element,row_id])#append
            elif '<bcc>' == element:
                next_element = entry[entry.index(element)+1] #next element is bcc email
                if next_element != "</bcc>": #make sure the next element is not the end tag
                    element = next_element.lower()
                    field = 'bcc'
                    if ',' in element:
                        element = element.split(',')
                        for elements in element:
                            emails.append([field,elements,row_id])
                    else:
                        emails.append([field,element,row_id])#append#append
 
    return emails    
 
def writeEmails(eList): #write emails.txt
    f = open("emails.txt","w+")
    for i in range(len(eList)):
        f.write(eList[i][0]+'-'+eList[i][1]+':'+eList[i][2]+'\n')
    f.close()
 
def createRecs(pList): #create the records
    recs =[]
    for entry in pList:
        for element in entry:
            element = element.lower() #lowercase
        row_id = entry[2] #the row_id is the 3 element in entry
        record = '' #create a whitespace var 
        record = record.join(entry) #join all entrys with whitespace var
        recs.append([row_id,record]) #append the records
    return recs
 
def writeRecs(rList):#write the recs.txt file
    f = open("recs.txt","w+")
    for i in range(len(rList)):
        f.write(rList[i][0]+':'+rList[i][1]+'\n')
    f.close()
 
main()
 
