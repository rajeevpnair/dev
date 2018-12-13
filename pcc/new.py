import imaplib
import email
import os
import datetime
from tabula import convert_into
import pandas
import numpy as np
import csv
 
svdir = os.getcwd()

mail=imaplib.IMAP4_SSL('imap-intern.telekom.de')
mail.login("rajeev.padinharepattu@t-systems.com","Ammukutt!2")
mail.select("INBOX")
date = date = datetime.datetime.now().strftime("%d-%b-%Y")

typ, msgs = mail.search(None, '(SENTON {date} FROM "Padinharepattu, Rajeev" SUBJECT "test_mail")'.format(date=date))
msgs = msgs[0].split()

for emailid in msgs:
    resp, data = mail.fetch(emailid, '(RFC822)')
    email_body = data[0][1] 
    email_body = email_body.decode('utf-8')
    m = email.message_from_string(email_body)
  
    for part in m.walk():
        filename = part.get_filename()
		
        if filename is not None:
            sv_path = os.path.join(svdir, filename)
			
            if not os.path.isfile(sv_path):
                print(sv_path)
                fp = open(sv_path, 'wb')
                fp.write(part.get_payload(decode=True))
                fp.close()
				
try:
	data
except NameError:
	print ("No Mails fount")
	exit()

else:
	for file in os.listdir(svdir):
		if file.endswith("xlsx"):
			files = (os.path.join(svdir, file))
			print (files)
