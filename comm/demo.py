import requests
import sys
import xml.etree.ElementTree as ET
from xml.etree import ElementTree
import random
import xmltodict
from datetime import datetime, timedelta
from datetime import datetime
import time
from random import randint
import base64
import json

service = 'http://52.172.42.201/webconsole/api/'

loginReq = '<DM2ContentIndexing_CheckCredentialReq username="Cvadmin" password="<<password>>" />'

pwd = 'Qwerty@123'
pwd = bytes(pwd, encoding='utf8')
pwd = str(base64.b64encode(pwd), encoding='utf-8')
loginReq = loginReq.replace("<<password>>", pwd)
   
r = requests.post(service + 'Login', data=loginReq)
print ("================================================================")
print ("================================================================")
token = None
if r.status_code == 200:
   root = ET.fromstring(r.text)
   if 'token' in root.attrib:
      token = root.attrib['token']
      print ("Login Successful")
   else:
      print ("Login Failed")
      sys.exit(0)
else:
   print ('there was an error logging in')
   print ("Logged in", r.status_code)
headers = {'Authtoken': token, 'Content-Type': 'application/xml'}

now = datetime.now()
hours_before = datetime.now() - timedelta(hours=12)

to_time = (int(time.mktime(now.timetuple())))
from_time = (int(time.mktime(hours_before.timetuple())))

def browse_client():
    
    '''
    #####find out a random cliend ID#####
    client_list = service + "Client"
    global headers
    r = requests.get(client_list, headers=headers)
    dic = (xmltodict.parse(r.text))
    print (dic)
    r_string = (str(r.text))
    r_string = (r_string.replace('clientId', ' data '))
    a = r_string.split()
    count1 = (a.count('data'))
    i = randint(0, count1-1)
    newclientId = (dic['App_GetClientPropertiesResponse']['clientProperties'][i]['client']['clientEntity']['@clientId'])
    '''

    schedules = service + "SchedulePolicy/207"
    global headers
    r = requests.get(schedules, headers=headers)
    r_string = (str(r.text))
    r_string = (r_string.replace('clientName', ' uniquekey '))
    a = r_string.split()
    count = (a.count('uniquekey'))
    dic = (xmltodict.parse(r.text))
    if count == 1:
        newclientId = dic['TMMsg_GetTaskDetailResp']['taskInfo']['associations']['@clientId']
    else:
        client_Id = []
        for i in dic['TMMsg_GetTaskDetailResp']['taskInfo']['associations']:
            client_Id.append(i['@clientId'])
        newclientId = random.choice(client_Id)
        
    subclient = service + "Subclient?clientId="+newclientId
    r = requests.get(subclient, headers=headers)
    r_string = (str(r.text))
    r_string = (r_string.replace('subClientProperties', ' data '))
    a = r_string.split()
    count1 = (a.count('data'))
    dic = (xmltodict.parse(r.text))
    
    if count1 == 2:
        subclientId = dic['App_GetSubClientPropertiesResponse']['subClientProperties']['subClientEntity']['@subclientId']
        backupsetId = dic['App_GetSubClientPropertiesResponse']['subClientProperties']['subClientEntity']['@backupsetId']
        backupsetName = dic['App_GetSubClientPropertiesResponse']['subClientProperties']['subClientEntity']['@backupsetName']
        instanceId = dic['App_GetSubClientPropertiesResponse']['subClientProperties']['subClientEntity']['@instanceId']
        applicationId = dic['App_GetSubClientPropertiesResponse']['subClientProperties']['subClientEntity']['@applicationId']
        clientId = dic['App_GetSubClientPropertiesResponse']['subClientProperties']['subClientEntity']['@clientId']
        clientName = dic['App_GetSubClientPropertiesResponse']['subClientProperties']['subClientEntity']['@clientName']
        print ("Searching on Server:",clientName,", Subclient:",backupsetName)
        
    else:
        count1 = int(count1/2)
        i = randint(0, count1-1)
        subclientId = dic['App_GetSubClientPropertiesResponse']['subClientProperties'][i]['subClientEntity']['@subclientId']
        backupsetId = dic['App_GetSubClientPropertiesResponse']['subClientProperties'][i]['subClientEntity']['@backupsetId']
        backupsetName = dic['App_GetSubClientPropertiesResponse']['subClientProperties'][i]['subClientEntity']['@backupsetName']
        instanceId = dic['App_GetSubClientPropertiesResponse']['subClientProperties'][i]['subClientEntity']['@instanceId']
        applicationId = dic['App_GetSubClientPropertiesResponse']['subClientProperties'][i]['subClientEntity']['@applicationId']
        clientId = dic['App_GetSubClientPropertiesResponse']['subClientProperties'][i]['subClientEntity']['@clientId']
        clientName = dic['App_GetSubClientPropertiesResponse']['subClientProperties'][i]['subClientEntity']['@clientName']
        print ("Searching on server:",clientName,", Subclient:",backupsetName)
        
        
    
    subclient_BROWSE = service + "Subclient/"+subclientId+"/Browse?path=%5C"
    headers = {'Authtoken': token}
    
    r = requests.get(subclient_BROWSE, headers=headers)
    if 'messages' in r.text:
        print ("There is no backups for the selected subclient, Selecting a new client")
        c = browse_client()
        return c
    
    else:
        r_string = (str(r.text))
        r_string = (r_string.replace('path', ' uniquekey '))
        a = r_string.split()
        count = (a.count('uniquekey'))
        jsonx = (xmltodict.parse(r.text))
        if count == 1:
            path = jsonx['databrowse_BrowseResponseList']['browseResponses'][0]['browseResult']['dataResultSet']['@path']
            print ("Path selected to search:", path)
        else:
            path1 = []
            for i in jsonx['databrowse_BrowseResponseList']['browseResponses'][0]['browseResult']['dataResultSet']:
                path1.append(i['@path'])
            path = random.choice(path1)
            print ("path selected to search:", path)
    
        return subclientId, backupsetId, backupsetName, instanceId, applicationId, clientId, clientName, path

c = browse_client()
c = list(c)
z = c[7]

def browse_data(c,z,to_time,from_time):
    
    path1 = []
    restore_file = []
    browse = service + "DoBrowse"
    xml ="""<databrowse_BrowseRequest opType="browse">
      <entity clientName="{}" applicationId="{}" clientId="{}" subclientId="{}" backupsetId="{}" instanceId="{}"/>
      <paths path="{}"/>
      <timeRange toTime="{}" fromTime="{}"/>
      <options showDeletedFiles="1" restoreIndex="1"/>
      <mode mode="2"/>
      <queries type="1" queryId="countQuery">
        <aggrParam aggrType="4" field="0"/>
      </queries>
      <queries type="0" queryId="dataQuery">
        <dataParam>
          <paging firstNode="0" skipNode="0" pageSize="15"/>
          <sortParam ascending="1">
            <sortBy val="38"/>
            <sortBy val="0"/>
          </sortParam>
        </dataParam>
      </queries>
    </databrowse_BrowseRequest>""".format(c[6],c[4],c[5],c[0],c[1],c[3],z,to_time,from_time)
    
    r = requests.post(browse, data=xml, headers=headers)
    r_string = (str(r.text))
    r_string = (r_string.replace('path', ' uniquekey '))
    a = r_string.split()
    count = (a.count('uniquekey'))
    jsonx = (xmltodict.parse(r.text)) 
    if count == 1:
        restore_file1 = []
        newpath = jsonx['databrowse_BrowseResponseList']['browseResponses'][1]['browseResult']['dataResultSet']['@path']
        size = jsonx['databrowse_BrowseResponseList']['browseResponses'][1]['browseResult']['dataResultSet']['@size']
        backup_date1 = jsonx['databrowse_BrowseResponseList']['browseResponses'][1]['browseResult']['dataResultSet']['advancedData']['@backupTime']

        if 'directory' in r.text:
            type1 = 'D'
        else:
            type1 = 'F'
            
        if int(size) < 10485760 and type1 == 'F':
            restore_file1 = newpath
        else:
            if int(size) > 0 and (type1) == 'D':
                path1 = newpath
                
        if restore_file1:
            print ("File to Restore is:", restore_file1)
            return restore_file1, c, backup_date1
        else:
            if path1:
                z = path1
                print ("Enter in to the child directory:", z)
                d = browse_data(c,z,to_time,from_time)
                return d
            
            else:
                c = ''
                c=browse_client()
                c = list(c)
                z=c[7]
                d = ''
                d = browse_data(c,z,to_time,from_time)
                return d

    else:
        newpath=[]
        size=[]
        type1=[]
        bdate=[]
        backup_date=[]
    
        if 'flags' in r.text:
            for i in jsonx['databrowse_BrowseResponseList']['browseResponses'][1]['browseResult']['dataResultSet']:
                newpath.append(i['@path'])
                size.append(i['@size'])
                bdate.append(i['advancedData']['@backupTime'])
                i22=0
                for i2 in i['flags']:
                    if i22==1: 
                      type1.append(i2) 
                    i22=i22+1
            
            for i in range(0,len(newpath)): 
                if int(size[i]) < 10485760 and (type1[i]) == '@file':
                    backup_date.append(bdate[i])
                    restore_file.append(newpath[i])
                    
    
                else:
                    if int(size[i]) > 0 and (type1[i]) == '@directory':
                        path1.append(newpath[i])
                        
            if restore_file:
                restore_file1 = random.choice(restore_file)
                backup_date1 = random.choice(backup_date)
                print ("file to restore is:", restore_file1)
                return restore_file1, c, backup_date1
                
            elif path1:
                random.shuffle(path1)

                for i in range(0,len(path1)):
                    z = path1[i]
                    print ("enter in to the child directory:", z)
                    d = browse_data(c,z,to_time,from_time)
                    return d

            else:
                print ("Browsing to new clients as no directries found with more than 0 bytes size")
                c = ''
                c=browse_client()
                c = list(c)
                z=c[7]
                d = browse_data(c,z,to_time,from_time)
                return d
                                    
        else:
            print ("Browsing to new client as no files, directries found in the current path")
            c = ''
            c=browse_client()
            c = list(c)
            z=c[7]
            d = browse_data(c,z,to_time,from_time)
            return d

d = browse_data(c,z,to_time,from_time)
restore_file2 = (d[0])
c = (d[1])
backup_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(d[2])))

restore_file2 = restore_file2.replace("\\", "\\\\")

def os_type(c):
    
    os = service + "Client/"+c[5]
    r = requests.get(os, headers=headers)
    dic = (xmltodict.parse(r.text))
    if (dic['App_GetClientPropertiesResponse']['clientProperties']['client']['osInfo']['@Type']) == 'Unix':
        dest_path = '/tmp'
        if (dic['App_GetClientPropertiesResponse']['clientProperties']['client']['osInfo']['@SubType']) == 'Linux':
            appTypeId = 29
        elif (dic['App_GetClientPropertiesResponse']['clientProperties']['client']['osInfo']['@SubType']) == 'Aix':
            appTypeId = 21
        elif (dic['App_GetClientPropertiesResponse']['clientProperties']['client']['osInfo']['@SubType']) == 'HP-UX':
            appTypeId = 17     
    elif (dic['App_GetClientPropertiesResponse']['clientProperties']['client']['osInfo']['@Type']) == 'Windows':
        appTypeId = 33
        dest_path = 'C:\\restore1'
    return appTypeId, dest_path

os = os_type(c)

def restore_data(c,os,from_time,to_time,restore_file2):
    
    print ("================================================================")
    print ("================================================================")
    print ("Restoring data started")
    print ("File:", restore_file2) 
    print ("On server:" ,c[6])
    print ("Destination path: [", os[1], "], On server: [",c[6],"]")
    print ("File backed up time:", backup_time)
    print ("================================================================")
    print ("================================================================")
    
    restore = service + "retrieveToClient"
    xml ="""<DM2ContentIndexing_RetrieveToClientReq mode="2" serviceType="1">
    <userInfo userGuid="4C1C8327-233F-46F5-910B-E873FBEBE494"/>
    <header>
    <srcContent clientId="{}" appTypeId="{}" instanceId="{}" backupSetId="{}" subclientId="{}" fromTime="{}" toTime="{}"/>
    <destination clientId="{}" clientName="{}" inPlace="0">
    <destPath val="{}"/>
    </destination>
    <filePaths val="{}"/>
    </header>
    <advanced restoreDataAndACL="1" restoreDeletedFiles="1"/>
    </DM2ContentIndexing_RetrieveToClientReq>""".format(c[5],os[0],c[3],c[1],c[0],from_time,to_time,c[5],c[6],os[1],restore_file2)
    
    r = requests.post(restore, data=xml, headers=headers)
    dictionary = (xmltodict.parse(r.text))
    jobId = dictionary['DM2ContentIndexing_RetrieveToClientResp']['@jobId']
    print ("Restore Job ID:", jobId)
    return jobId

k = restore_data(c,os,from_time,to_time,restore_file2)

print ("waiting to complete the restore")
time.sleep(60)

def job_status(k):
    job = service + "Job/"+k
    r = requests.get(job, headers=headers)
    dictionary = (xmltodict.parse(r.text))
    job_status = dictionary["JobManager_JobListResponse"]["jobs"]["jobSummary"]["@localizedStatus"]
    return job_status

j = job_status(k)
print ("Restoration status:", j)
print ("================================================================")
print ("================================================================")
