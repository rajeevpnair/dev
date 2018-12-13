import imaplib
import email
import os
import datetime
import pickle

 
svdir = os.getcwd()

mail=imaplib.IMAP4_SSL('imap-intern.telekom.de')
mail.login("rajeev.padinharepattu@t-systems.com","Ammukutt!2")
mail.select("INBOX")

date = date = datetime.datetime.now().strftime("%d-%b-%Y")

typ, msgs = mail.search(None, '(SENTON {date} FROM "Padinharepattu, Rajeev" SUBJECT "test_mail")'.format(date=date))

print (msgs)

msgs = msgs[0].split()

for emailid in msgs:
	resp, data = mail.fetch(emailid, '(RFC822)')
	email_body = data[0][1]
	email_body = email_body.decode()
	b = email.message_from_string(email_body)
	output = open('test.html', 'wb')
	pickle.dump(b, output)
	output.close()
