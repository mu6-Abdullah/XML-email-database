from bsddb3 import db
#Grab the phase 2 code an rerun it to get the new IDX's, then use those as the idx, then compare 
def main():
    print("\nWelcome! This program was created by Muhammad Abdullah and Adam Elamy for CMPUT 291 taught by Davood Rafiei!\n")
    recs = db.DB() #create an instance of recs
    emails = db.DB() #create an instance of emails
    dates = db.DB() #dates
    terms = db.DB() #terms
    databases = [recs,emails,dates,terms]
    db_files = ["re.idx","em.idx","da.idx","te.idx"] #these are all the db indexes
    for x in range(len(db_files)):
        databases[x].set_flags(db.DB_DUP)
        if x == 0:
            databases[x].open(db_files[x],None, db.DB_HASH, db.DB_CREATE) #create db files for indexes
        else:
            databases[x].open(db_files[x],None, db.DB_BTREE, db.DB_CREATE) #create db files for binary trees
    u_db = User_DB(recs,emails,dates,terms)
    u_db.run()
    for database in databases:
        database.close()
    print("Thank you for using our database! Have a great day!")
class User_DB:
    def __init__(self,recs,emails,dates,terms):
        self.recs = recs #initialize a database for recs,emails,terms,dates
        self.emails = emails
        self.terms = terms
        self.dates = dates
        self.full = False #output is brief
        self.list = [0] # a list of of all the things to return

    def run(self): #run the interface
        loop = True #while this var is true
        while loop: 
            return_list = self.create_interface() #create an individual interface that returns user input
            if return_list == 0: #if there is nothing returned NO USER INPUT
                loop = False #exit the loop
            elif loop: #otherwise 
                self.process_query(return_list) #Process the user input
                final_list = self.intersection() #get all the possible intersections
                self.print_output(final_list) #print the final output

    def print_output(self, final_list): #Assume everything works
        #create an output from final_list
        #Assuming final_list contains the row_id 
        #traverse the list backwards and append all the values to a dictionary
        #print(final_list)
        if len(final_list) != 0:
            curs = self.recs.cursor()
            for x in range(len(final_list)):
                iter = curs.set(final_list[x])
                r_id = str(iter[0].decode("utf-8"))
                record = str(iter[1].decode("utf-8"))
                if not self.full:
                    record = record.split("<subj>")
                    if len(record) != 1:
                        x = record[1]
                        x = x.split("</subj>")
                        record = x[0]
                    else:
                        record = ''
                if x == 1:
                    print()
                print("Record #:",r_id)
                print("Record:\n",(record.strip()))
                print()
        else: 
            print("No records match that query at this time!\n")

        #If self.full print the full record with id 
        #otherwise print just the id and subject 

    def create_interface(self): #create an individual interface
        self.reset()
        options = ["A user can enter:","[output=brief] (default) or [output=full] to change the output format","[\q/] or [\Q/] to quit"]
        loop = True
        while loop: #while loop is false
            for item in options:
                print(item)
            user_input = input("Enter a command > ").strip().lower() #Take the input and convert to lowercase
            user_input = user_input.replace("\\","&92;")
            return_list = self.valid_input(user_input) #the return list value should be the user_input
            if return_list == [0]:
                loop = False
                return 0
            elif return_list == [1] or return_list == [2]: #this is not necessary, but is more for stylistic purposes
                loop = True #continue the loop
                file_format = "BRIEF"
                if self.full:
                    file_format = "FULL"
                print("\nFile format reconfigured to:", file_format)
                print()
            else:
                loop = False #stop the loop if the return value is not 1
        
        print()#prints 2 new lines after printing a menu
        #print(return_list)
        return return_list
    
    def process_query(self,return_list): #given user_input determine what queries to search
        for x in range(len(return_list)):
            try:
                k,v = return_list[x]
            except ValueError:
                value = return_list[x][0]
                delims = [":",">","<",">=","<="]
                done = False
                x = 0
                length = len(delims)
                while x < length and not done:
                    if delims[x] in value:
                        
                        query = value.split(delims[x])
                        k = query[0] + delims[x]
                        v = query[1]
                        done = True
                    x += 1
                if not done:
                    k = value
            # try:
            #     v == 5
            #     print(v)
            # except NameError:
            #     pass
            
            if k == 'to:':
                self.get_emails(v,"to")
            elif k == "from:":
                self.get_emails(v,"from")
            elif k == "bcc:":
                self.get_emails(v,"bcc")
            elif k == "cc:":
                self.get_emails(v,"cc")
            elif k == "date:":
                self.get_dates(v)
            elif k == "date<":
                self.get_smaller_dates(v,1)
            elif k == "date<=":
                self.get_smaller_dates(v,2)
            elif k == "date>":
                self.get_bigger_dates(v,1)
            elif k == "date>=":
                self.get_bigger_dates(v,2)
            elif k == "subj:":
                self.get_terms("s-"+v)
            elif k == "body:":
                self.get_terms("b-"+v)
            elif '%' in k:
                self.get_partial_matching(k[0:(len(k) - 1)])
                self.get_partial_matching(k[0:(len(k) - 1)],1)
            else:
                self.get_terms("b-"+k)
                self.get_terms("s-"+k,1)
    
    def get_partial_matching(self,term,code = 0):
        curs = self.terms.cursor()
        if code == 0:
            self.list[0] += 1
            string = "b-" + term
        else:
            string = "s-" + term
        encoded_string = string.encode("utf-8")
        iter = curs.first()
        
        while iter:
            value = str(iter[0].decode("utf-8")) 
            cut_value = value[0:len(string)]
            if cut_value == string:
                self.list.append(iter[1])

            iter = curs.next()
        curs.close()
        # Brand new function
        # attempting to get all the records corresponding 
        # 
        
    def get_recs(self,recs): # selflist contains everything, 
        # Everytime you call self.list, there is a note on how many things you should increment
        self.list[0] +=1
        curs = self.recs.cursor() # get the cursor onto the recs index
        string = term.encode("utf-8")
        iter = curs.set(string) # encode according to utf-8 format
        while iter:
            if iter[0] == string:
                self.list.append(iter[1]) 
            iter = curs.next()
        curs.close()

    def get_terms(self,term,code = 0): #grabs all the terms
        if code == 0:
            self.list[0] += 1 #increment self.list by 1
        curs = self.terms.cursor() #put the cursor on the terms index
        string = term.encode("utf-8")
        iter = curs.set(string) #encode according to utf-8
        while iter:
            
            #print("Iter is",iter)
            value = (iter[0].decode("utf-8"))
            #value = value.decode("utf-8")
            #print("Value is ", value)
            #print("Term is ",term)
            if term == value:
                #print(term)
                self.list.append(iter[1])
            
            iter = curs.next()
        curs.close()

    def get_smaller_dates(self,date,code):
        self.list[0] += 1 #incremenet self.list
        curs = self.dates.cursor()
        iter = curs.first() 
        while iter:
            value = (str(iter[0].decode("utf-8")))
            if (code == 1 and value < date) or (code == 2 and value <= date):
                self.list.append(iter[1])
            else:
                break
            iter = curs.next()
        curs.close()

    def get_bigger_dates(self,date,code): #
        self.list[0] += 1 #increment self.list
        curs = self.dates.cursor() #put the cursor onto dates
        iter = curs.last() #encode in utf-8
        while iter:
            value = (str(iter[0].decode("utf-8")))
            if (code == 1 and value > date) or (code == 2 and value >= date):
                self.list.append(iter[1])
            else:
                break
            iter = curs.prev()
        curs.close()

    def get_dates(self,date):
        self.list[0] += 1 #increment self.list
        curs = self.dates.cursor()#put the cursor on dates
        string = date.encode("utf-8")
        iter = curs.set(string) #encode in utf-8
        while iter:
            value = iter[0]
            if value == string:
                self.list.append(iter[1])      
            iter = curs.next()
        curs.close()

    def get_emails(self,email,value): #grab emails
        code = 0
        if value == "cc":
            code = 1
        self.list[0] += 1 #increment the list

        curs = self.emails.cursor() #grab the emails index
        iter = curs.first() #encode according to utf-8
        while iter: #continue while the iter does not equal none
            item = str(iter[0].decode("utf-8"))
            if value in item:
                if code == 1 and 'bcc' not in item:
                    if email == item.strip(value+'-'): 
                        self.list.append(iter[1]) #append the value to the list
                elif code == 0 and email == item.strip(value+'-'):
                    self.list.append(iter[1])
            iter = curs.next() #go to the next value
        curs.close()

    def intersection(self):
        d = {} # d is a dict
        final_list = [] #final_list is a list
        #print(self.list)
        for x in range(1,len(self.list)):  #in the range of the length of the list
            if self.list[x] not in d: #if an element of the list is not in the the dict
                d[self.list[x]] = 1 # say that the count of that element is 1
            elif self.list[x] in d: #otherwise if its in
                d[self.list[x]] += 1 #increment by one
        for k,v in d.items(): #for all the items
            if v >= self.list[0]: #if the v = self.list[0]
                final_list.append(k) #append k to the v
        return final_list #return the list

    def reset(self):
        self.list = [0]

    def valid_input(self,user_input): # def the valid_input
        if 'output' in user_input: 
            if 'brief' in user_input:#if output==brief is in user_input
                self.full = False
                return [1]
            elif 'full' in user_input: #output full statements if output==full ins user_input
                self.full = True
                return [2]
        if "\q/" in user_input:
            return [0]
        user_input = user_input.split() #split the user input at newline characters
        nice_input = [] #
        final_input = []
        delims = [":",">","<",">=","<=","%"] 
        
        for x in range(len(user_input)):
            if (x == 0 or user_input[x] not in delims) and user_input[x][0] not in delims: #if its the first element or element in the list and is not a delim
                nice_input.append(user_input[x]) #append it to nice list
            elif user_input[x] in delims: #otherwise
                delim = delims[delims.index(user_input[x])] #append delim to prev value
                value = nice_input[x - 1] 
                nice_input[x - 1] = value + delim
            elif user_input[x][0] in delims:
                delim = delims[delims.index(user_input[x][0])]
                value = nice_input[x - 1]
                nice_input[x - 1] = value + delim
                nice_input.append(user_input[x][1:len(user_input[x])])

        
        x = 0
        date_headers = ["date:","date>","date<","date>=","date<="] #all possible values in inputs for dates
        email_headers = ["from:","to:","cc:","bcc:"] #all possible sections for finding emails
        term_headers = ["subj:","body:"] #all possible sections for 
        while x < len(nice_input): 
            current_value = nice_input[x]
            if current_value in date_headers or current_value in email_headers or current_value in term_headers: #if the value is any one if these headers
                if len(final_input) == 0:
                    final_input.append([current_value,nice_input[x + 1]]) #append it and append the next element
              
                    x += 2 #incremenet by 2
            else: #otherwise there is 2 cases
                #an individual word with % 
                #an individual word
                final_input.append([current_value])
                x += 1
       
            
        return final_input
        
main()