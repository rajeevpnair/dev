import pandas as pd
import os
import win32com.client
import time
from pandas import ExcelWriter
import pickle

mail_subject = "subjectpdf"
outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
inbox = outlook.GetDefaultFolder(6)
inbox_sub = inbox.Folders("testbox")
messages = inbox_sub.Items
message = messages.GetLast()
body = message.body
output = open('test.txt', 'wb')
pickle.dump(body, output)
output.close()
with open('test.txt')as fin, open('test2.txt', 'w') as fout:
	for line in fin:
		fout.write(line.replace("	", " "))
		
file = open("test2.txt", "r")
for line in file:
	fields = line.split(" ")
	if fields[0] == 'Backup' and fields[2] == 'Failed':
			print (fields[0], fields[2], 'for', fields[1])
file.close()

#Delete the attachments from the local system
os.remove(os.getcwd() + '\\' + 'test2.txt')
os.remove(os.getcwd() + '\\' + 'test.txt')
