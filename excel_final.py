import win32com.client
import time
import os
import pandas as pd
import xlrd
from pandas import ExcelWriter

mail_subject = "subject"
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
	attachments = message.attachments
	attachment = attachments.Item(1)
	if subject == mail_subject and received_date == today:
		attachment.SaveASFile(os.getcwd() + '\\' + str(attachment))
		df = pd.read_excel( (os.getcwd() + '\\' + str(attachment)) , sheet_name='Sheet1')
		Job_status = ['Failed', 'Partially Successful']
		failed_jobs = df[[x in Job_status for x in df['Job Status']]]
		break
		
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
os.remove(os.getcwd() + '\\' + str(attachment))
