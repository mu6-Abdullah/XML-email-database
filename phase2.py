import os
def main():
    files = ['terms.txt','emails.txt','dates.txt','recs.txt'] #list of files
    index_files = ["te.idx","em.idx","da.idx","re.idx"] #list of index outputs
    
    for x in range(len(files)):
        s_file_name = files[x].replace(".txt","_sorted.txt")
        sort(files[x],s_file_name) #takes the file and gets rid of duplicates and replaces the file with the sorted file
        load_file_name = s_file_name.replace("_sorted.txt","_load_ready.txt")
        splitter(s_file_name,load_file_name) #use the splitter function to sort the data properly
        if x != 3:
            index_maker(load_file_name,"btree",index_files[x]) #create B+ trees for dates,terms, emails
        elif x == 3:
            index_maker(load_file_name,"hash",index_files[x]) #create a hash index for recs
 
 
def splitter(s_file_name,load_file_name):
    
    file = open(s_file_name)
    file1 = open(load_file_name,'w')

    for line in file:
        line = line.strip()
        line = line.replace("\\","&92;")
        line1 = line.split(':',1)
        if s_file_name != 'recs_sorted.txt':
            try:
                int(line1[1])
            except:
                line1 = line.split(':')
                line1 = [':'.join(line1[0:(len(line1) - 1)]),line1[len(line1) - 1]]
        key = line1[0]
        value = line1[1]
        file1.write(key+'\n')
        file1.write(value+'\n')
    file.close()
    file1.close()

def sort(file_name,s_file_name):
    os.system("sort %s -u > %s" % (file_name,s_file_name))
 
def index_maker(file_name,type_index,output):
    string = "db_load -c duplicates=1 -T -t %s -f %s %s" % (type_index,file_name,output)
    os.system(string)
main()
