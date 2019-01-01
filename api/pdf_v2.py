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
mail.login("ajay-kumar.ay@t-systems.com","Password!1")
mail.select("INBOX")


date = date = datetime.datetime.now().strftime("%d-%b-%Y")

def api():
    
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

    userAndPass = b64encode(b"rrawat:Welcome8").decode("ascii")
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
    #print(xmlDocument)
    root = ET.fromstring(xmlDocument)
    incidentId = root.find("Body/CreateTsiIncidentResponse/model/instance/IncidentID")
    print('Incident ID : '+ incidentId.text)
    return

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
                        title = ''.join(('server ', (df2.iat[i,1]), ' ', (df2.iat[i - 1 ,5]), (df2.iat[i,5])))
                        print (title)
                        description = "yet to be decided"
                        api()
                        i = i + 1
                    else:
                        title = ''.join(('server ', (df2.iat[i,1]), ' ', (df2.iat[i,5])))
                        print (title)
                        description = "yet to be decided"
                        api()
                        i = i + 1
			
                i = n+1
	
                while (i <= n2 - 1):
                    if df2.iat[i,3] == 'null_value':
                        i = i + 1
                        title = ''.join(('network device ', (df2.iat[i,1]), ' ', (df2.iat[i - 1 ,5]), (df2.iat[i,5])))
                        print (title)
                        description = "yet to be decided"
                        api()
                        i = i + 1
                    else:
                        title = ''.join(( 'network device ', (df2.iat[i,1]), ' ', (df2.iat[i,5])))
                        print (title)
                        description = "yet to be decided"
                        api()
                        i = i + 1
			#Delete the attachments from the local system
            os.remove(files)
