import imaplib
import email
import os
import datetime
from tabula import convert_into
import pandas
import numpy as np
import csv

svdir = os.getcwd()
filename = 'None'
mail=imaplib.IMAP4_SSL('imap-intern.telekom.de')
mail.login("rajeev.padinharepattu@t-systems.com","Ammukutt!2")
mail.select("INBOX")

date = date = datetime.datetime.now().strftime("%d-%b-%Y")

typ, msgs = mail.search(None, '(SENTON {date} FROM "Padinharepattu, Rajeev" SUBJECT "pcc_pdf")'.format(date=date))
count = len(msgs[0].split())

for num in msgs[0].split():
    typ, data = mail.fetch(num, '(RFC822)')
    email_body = data[0][1] 
    email_body = email_body.decode('utf-8')
    m = email.message_from_string(email_body)
 
    if m.get_content_maintype() != 'multipart':
        continue
 
    for part in m.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue
 
    filename=part.get_filename()
    if filename is not None:
        sv_path = os.path.join(svdir, filename)
        if not os.path.isfile(sv_path):
            print(sv_path)
            fp = open(sv_path, 'wb')
            fp.write(part.get_payload(decode=True))
            fp.close()
                
if count == 0:
    print ('No mails found')
    sys.exit()
else:
    for file in os.listdir(svdir):
        if file.endswith(".pdf"):
            files = (os.path.join(svdir, file))
            convert_into(files, "test.csv", output_format="csv", multiple_tables=True)
            df2 = pandas.read_csv("test.csv")
            df2 = df2.replace(np.nan, 'null_value')
            n2 = (df2.shape[0])
			
            for i in range(1,n2):
                if df2.iat[i,1] == 'host':
                    break
				
            n = i
            print('')
            print('')
			
            try:
                df2
            except NameError:
                print ("There are no failed jobs reported")
                exit()
				
            else:
                i = 0
                while (i < n):
                    if df2.iat[i,3] == 'null_value':
                        i = i + 1
                        description = ('server ', (df2.iat[i,1]), ' ', (df2.iat[i - 1 ,5]), (df2.iat[i,5]))
                        description = ''.join(description)
                        print (description)
                        i = i + 1
                    else:
                        description = ('server ', (df2.iat[i,1]), ' ', (df2.iat[i,5]))
                        description = ''.join(description)
                        print (description)
                        i = i + 1
			
                i = n+1
	
                while (i <= n2 - 1):
                    if df2.iat[i,3] == 'null_value':
                        i = i + 1
                        description = ('network device ', (df2.iat[i,1]), ' ', (df2.iat[i - 1 ,5]), (df2.iat[i,5]))
                        description = ''.join(description)
                        print (description)
                        i = i + 1
                    else:
                        description = ( 'network device ', (df2.iat[i,1]), ' ', (df2.iat[i,5]))
                        description = ''.join(description)
                        print (description)
                        i = i + 1
			#Delete the attachments from the local system
            os.remove(files)
