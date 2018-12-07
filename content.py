import os
import win32com.client
import time
import pickle

mail_subject = "subjectpdf"
outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
inbox = outlook.GetDefaultFolder(6)
inbox_sub = inbox.Folders("testbox")
messages = inbox_sub.Items
message = messages.GetLast()
subject = message.Subject
today = time.strftime('%Y-%m-%d')
received_date = message.ReceivedTime.strftime("%Y-%m-%d")

for message in list(messages):
	subject = message.Subject
	received_date = message.ReceivedTime.strftime("%Y-%m-%d")
	body = message.body
	if subject == mail_subject and received_date == today:
		mail_status = 'yes'
		output = open('test.txt', 'wb')
		pickle.dump(body, output)
		output.close()
		with open('test.txt')as fin, open('test2.txt', 'w') as fout:
			for line in fin:
				fout.write(line.replace("	", " "))
		break
	
try:
  mail_status
except NameError:
  print ("No Mails found with subject ", mail_subject)
  exit()
  
file = open("test2.txt", "r")
for line in file:
	fields = line.split(" ")
	if fields[0] == 'Backup' and fields[2] == 'Failed':
		description = (fields[0], ' ', fields[2], ' for ',fields[1])
		description = ''.join(description)
		print (description)
file.close()

try:
  description
except NameError:
  print ("There are no failed jobs reported")
 
#Delete the attachments from the local system
os.remove(os.getcwd() + '\\' + 'test2.txt')
os.remove(os.getcwd() + '\\' + 'test.txt')
