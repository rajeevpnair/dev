import imaplib
import email
import os
import datetime
import pandas as pd
import sys
import requests
import json
from base64 import b64encode
import xml.etree.ElementTree as E
import json
 
svdir = os.getcwd()
filename = 'None'
mail=imaplib.IMAP4_SSL('imap-intern.telekom.de')
mail.login("rajeev.padinharepattu@t-systems.com","Ammukutt!2")
mail.select("INBOX")

date = date = datetime.datetime.now().strftime("%d-%b-%Y")

typ, msgs = mail.search(None, '(SENTON {date} FROM "Padinharepattu, Rajeev" SUBJECT "pcc_excel")'.format(date=date))
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
           # print(sv_path)
            fp = open(sv_path, 'wb')
            fp.write(part.get_payload(decode=True))
            fp.close()
                
if count == 0:
    print ('No mails found')
    sys.exit()
else:
    for file in os.listdir(svdir):
        if file.endswith(".xlsx"):
            files = (os.path.join(svdir, file))
            df = pd.read_excel(files, sheet_name='Sheet1')
            Job_status = ['Failed', 'Partially Successful']
            failed_jobs = df[[x in Job_status for x in df['Job Status']]]
            
            try:
                failed_jobs
            except NameError:
                print ("There are no failed jobs reported")
                print()
            else:
                n = (failed_jobs.shape[0])
                i = 0
                while (i < n):
                    description = ''.join(((failed_jobs.iat[i,9]), ' backup ', (failed_jobs.iat[i,4]), ' for Client server ', (failed_jobs.iat[i,2]), ', Master server is ', (failed_jobs.iat[i,0])))
                    title = ''.join(('Backup error for ', (failed_jobs.iat[i,2])))
                    CI = (failed_jobs.iat[i,2])
                    url = 'https://6.152.112.14:8443/oo/rest/v2/executions/'
                    data = '''{
                    "flowUuid":               "114ae4a6-e2cf-47e6-97e7-a76a6e153439", 
                    "runName":                "AOC_create_INM_run_1234",
                    "logLevel":               "STANDARD", 
                    "inputs": {
                            "assignmentGroup":     "C.DPS.MY.CCO.SH.WIN.EVT",
                            "customer":            "SHELL/SHELL",
                            "title":               "'''+ title +'''",
                            "category1":           "???",
                            "category2":           "?",
                            "causingCI":           "'''+ CI +'''",
                            "description":         "'''+ description +'''",
                            "reportedByUserId":    "rrawat",
                            "reportedByLastName":  "Rawat",
                            "reportedByFirstName": "Rajat",
                            "contactLastName":     "Rawat",
                            "contactFirstName":    "Rajat",
                            "criticality":         "LOW",
                            "serviceRestriction":  "LOW",
                            "openGroup":           "C.SH.MY.WIN.EVT",
                            "priority":            "4",
                            "Urgency":             "Low"
                            
                            }
                    }'''

                    proxies = {
                            "http": None,
                            "https": None,
                            }

                    userAndPass = b64encode(b"rrawat:Welcome7").decode("ascii")
                    headers = {'Content-Type': 'application/json', 'Authorization' : 'Basic %s' %  userAndPass }
                    jobid = requests.post(url, data=data, headers=headers, verify=False, proxies=proxies)
                    print('Job ID : ' + str(jobid.text))
                    url = 'https://6.152.112.14:8443/oo/rest/v2/executions/{0}/execution-log'.format(jobid.text)
                    print(url)
                    jsonDoc = ''
                    # run job until result is ok
                    stat='RUNNING'
                    j=0
                    while stat == 'RUNNING' :
                        time.sleep(1)
                        j=j+1
                        print(str(j) + ' ')
                        jsonDoc = requests.get(url, headers=headers, verify=False, proxies=proxies)
                        executionSummaryDict = json.loads(jsonDoc.text)
                        stat = executionSummaryDict["executionSummary"]["status"]
                        print('status: '+stat)
                        
                    summaryDict = json.loads(jsonDoc.text)
                    xmlDocument = summaryDict["flowOutput"]["document"]
                    print(xmlDocument)
                    root = ET.fromstring(xmlDocument)
                    incidentId = root.find("Body/CreateTsiIncidentResponse/model/instance/IncidentID")
                    print('Incident ID : '+ incidentId.text)
                    i = i + 1
            os.remove(files)
