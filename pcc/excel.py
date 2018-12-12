import imaplib
import email
import os
import datetime
 
svdir = os.getcwd()

mail=imaplib.IMAP4_SSL('imap-intern.telekom.de')
mail.login("rajeev.padinharepattu@t-systems.com","Ammukutt!2")
mail.select("INBOX")

date = date = datetime.datetime.now().strftime("%d-%b-%Y")

typ, msgs = mail.search(None, '(SENTON {date} FROM "SV, Aneesh" SUBJECT "test_mail")'.format(date=date))

print (msgs)

msgs = msgs[0].split()

for emailid in msgs:
    resp, data = mail.fetch(emailid, '(RFC822)')
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
				
				df = pd.read_excel( (os.getcwd() + '\\' + str(filename)) , sheet_name='Sheet1')
				Job_status = ['Failed', 'Partially Successful']
				failed_jobs = df[[x in Job_status for x in df['Job Status']]]
				try:
					failed_jobs
				except NameError:
					print ("There are no failed jobs reported")
					exit()
				else:
					n = (failed_jobs.shape[0])
					i = 0
					while (i < n):
						description = ((failed_jobs.iat[i,9]), ' backup ', (failed_jobs.iat[i,4]), ' for Client server ', (failed_jobs.iat[i,2]), ', Master server is', (failed_jobs.iat[i,0]))
						description = ''.join(description)
						print (description)
						i = i + 1
				#Delete the attachments from the local system
				os.remove(os.getcwd() + '\\' + str(filename))
