import imaplib
import email
import os
import datetime
import pickle
import pandas as pd

 
svdir = os.getcwd()

mail=imaplib.IMAP4_SSL('imap-intern.telekom.de')
mail.login("rajeev.padinharepattu@t-systems.com","Ammukutt!2")
mail.select("INBOX")

date = date = datetime.datetime.now().strftime("%d-%b-%Y")

typ, msgs = mail.search(None, '(SENTON {date} FROM "Padinharepattu, Rajeev" SUBJECT "test_mail_content")'.format(date=date))



msgs = msgs[0].split()
i = 0
for emailid in msgs:
	resp, data = mail.fetch(emailid, '(RFC822)')
	email_body = data[0][1]
	email_body = email_body.decode('utf-8')
	b = email.message_from_string(email_body)
	output = open('test.html', 'wb')
	pickle.dump(b, output)
	output.close()
    
try:
	data
except NameError:
	print ("No Mails fount")
	exit()
else:
    for file in os.listdir(svdir):
        if file.endswith(".html"):
            files = (os.path.join(svdir, file))
            pd.set_option('display.expand_frame_repr', False)
            df = pd.read_html('test.html', encoding='utf')
            df = df[0].dropna(axis=0, thresh=4)
            df.columns = df.iloc[0]
            col = ['Specification','Session Type', 'Mode', 'Status', 'Start Time', 'Duration', 'GB Written', '# Files', '# Warnings', '# Errors', 'Duration']
            df[col] = df[col].replace({'=':''}, regex=True)
            df = df.loc[df['Status'] == 'Failed']
            print (df['Session ID'])
            n = (df.shape[0])
            i = 0
            while (i < n):
                description = ('Session Type: ', df.iat[i,0], '\n' 'Specification: ', df.iat[i,1], '\n' 'Status: ', df.iat[i,2])
                description = ''.join(description)
                ticket_description = ('Ticket_description:', df.iat[i,0], ' failed for', df.iat[i,1], ' (Session ID ', df.iat[i,14], ')', '\n')
                ticket_description = ''.join(ticket_description)
                print (description)
                print (ticket_description)
                i = i + 1
            os.remove(files)
