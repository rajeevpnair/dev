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
    attachment.SaveASFile(os.getcwd() + '\\' + str(attachment))
    df = pd.read_excel('Book1.xlsx' , sheet_name='Sheet1')
    Job_status = ['Failed', 'Partially Successful']
    failed_jobs = df[[x in Job_status for x in df['Job Status']]]
    print (failed_jobs)
    if subject == mail_subject and received_date == today:
	       break

print ("Didn't find any mails with subject mail_subject from sender mail_sender")
os.remove(attachment)
