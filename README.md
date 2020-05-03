# XML-email-database
phase1.py parses XML email records, parses data to txt files
          using itertools and sys library
Created 4 Txt files:
          terms.txt, dates.txt, emails.txt, recs.txt
          
phase2.py creates hash and binary indexes from the previously created txt files.
          uses Berkeley DB and os library
Created 4 Indexes:
          B+ trees:
          dates, terms, emails
          Hash Index:
          recs
          Outputs: te.idx, em.idx, da.idx, re.idx          
          
phase3.py parse through the indexes and perform search queries for data entries in different parts of email records
          using Berkeley DB 
          
          
This project was a collaboration with Adam-Elamy (elmay1@ualberta.ca)          
