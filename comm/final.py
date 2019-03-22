import requests
import sys
import xml.etree.ElementTree as ET
from xml.etree import ElementTree
import random
import xmltodict
import json
from datetime import datetime, timedelta
from datetime import datetime
import time


from random import randint

import base64
import json
global b

service = 'http://13.71.81.222/webconsole/api/'

loginReq = '<DM2ContentIndexing_CheckCredentialReq username="Cvadmin" password="<<password>>" />'

pwd = 'Qwerty@123'
pwd = bytes(pwd, encoding='utf8')
pwd = str(base64.b64encode(pwd), encoding='utf-8')
loginReq = loginReq.replace("<<password>>", pwd)
   
r = requests.post(service + 'Login', data=loginReq)
print ("==========================================================================")
token = None
print (r)
if r.status_code == 200:
   root = ET.fromstring(r.text)
   if 'token' in root.attrib:
      token = root.attrib['token']
      print ("Login Successful")
      print (r.status_code)
   else:
      print ("Login Failed")
      print (r.status_code)
      sys.exit(0)
else:
   print ('there was an error logging in')
   print ("Logged in", r.status_code)
headers = {'Authtoken': token, 'Content-Type': 'application/xml'}

now = datetime.now()
hours_before = datetime.now() - timedelta(hours=100)

to_time = (int(time.mktime(now.timetuple())))
from_time = (int(time.mktime(hours_before.timetuple())))

def browse_client():

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
        print ("Searching on client:", newclientId)
    else:
        client_Id = []
        for i in dic['TMMsg_GetTaskDetailResp']['taskInfo']['associations']:
            client_Id.append(i['@clientId'])
        newclientId = random.choice(client_Id)
        print ("Searching on client:", newclientId)
        
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
        print ("One sbclient only", subclientId, backupsetId, backupsetName, instanceId, applicationId, clientId, clientName)
        
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
        print ("Selected from multiple subclients", subclientId, backupsetId, backupsetName, instanceId, applicationId, clientId, clientName)
        
        
    
    subclient_BROWSE = service + "Subclient/"+subclientId+"/Browse?path=%5C"
    headers = {'Authtoken': token}
    
    r = requests.get(subclient_BROWSE, headers=headers)
    json1 = (xmltodict.parse(r.text))
    if 'messages' in r.text:
        print ("There is no backups for the selected subclient")
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
            print ("Only one base path:", path)
        else:
            path1 = []
            for i in jsonx['databrowse_BrowseResponseList']['browseResponses'][0]['browseResult']['dataResultSet']:
                path1.append(i['@path'])
            path = random.choice(path1)
            print ("Selected from multiple paths:", path)
    
        return subclientId, backupsetId, backupsetName, instanceId, applicationId, clientId, clientName, path

c = browse_client()
print ("all details from client:", c)

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
        newpath = jsonx['databrowse_BrowseResponseList']['browseResponses'][1]['browseResult']['dataResultSet']['@path']
        size = jsonx['databrowse_BrowseResponseList']['browseResponses'][1]['browseResult']['dataResultSet']['@size']
        check = jsonx['databrowse_BrowseResponseList']['browseResponses'][1]['browseResult']['dataResultSet']['flags']
        if 'file' in check:
            type1 = '@file'
        else:
            type1 = '@directory'
            
        if int(size) < 10485760 and type1 == '@file':
            restore_file = newpath
        else:
            if int(size) > 0 and (type1) == '@directory':
                path1 = newpath
                
        if restore_file:
            restore_file1 = random.choice(restore_file)
            print ("restore fils of less than 10MB single file:", restore_file)
            return restore_file1, c
        else:
            if path1:
                z = path1
                print ("enter in to the directory", z)
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
    
        if 'flags' in r.text:
            for i in jsonx['databrowse_BrowseResponseList']['browseResponses'][1]['browseResult']['dataResultSet']:
                newpath.append(i['@path'])
                size.append(i['@size'])
                i22=0
                for i2 in i['flags']:
                    if i22==1: 
                      type1.append(i2) 
                    i22=i22+1
            
            for i in range(0,len(newpath)): 
                if int(size[i]) < 10485760 and (type1[i]) == '@file':
                    restore_file.append(newpath[i])
    
                else:
                    if int(size[i]) > 0 and (type1[i]) == '@directory':
                        path1.append(newpath[i])
                        
            if restore_file:
                restore_file1 = random.choice(restore_file)
                print ("restore fils of less than 10MB multiple file", restore_file)
                return restore_file1, c
                
            elif path1:
                print ("directory of size more than 0 MB", path1)
                random.shuffle(path1)

                for i in range(0,len(path1)):
                    z = path1[i]
                    print (" browsing with new path", z)
                    d = browse_data(c,z,to_time,from_time)
                    return d

            else:
                print ("Browsing 2 new clients as no directries found with more than 0 bytes size")
                c = ''
                c=browse_client()
                c = list(c)
                z=c[7]
                d = browse_data(c,z,to_time,from_time)
                return d
                                    
        else:
            c = ''
            c=browse_client()
            c = list(c)
            z=c[7]
            d = browse_data(c,z,to_time,from_time)
            return d

d = browse_data(c,z,to_time,from_time)

restore_file2 = (d[0])
c = (d[1])

print (c)
print (restore_file2)

def os_type(c):
    
    os = service + "Client/"+c[5]
    print (c[5])
    r = requests.get(os, headers=headers)
    print (r.status_code)
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
        dest_path = 'C:\\temp'
    return appTypeId, dest_path

os = os_type(c)

def restore_data(c,os,from_time,to_time,restore_file2):
    
    print ("================================================================")
    print ("================================================================")
    print ("Restoring data started")
    print ("File:", restore_file2) 
    print ("On server:" ,c[6])
    print ("Destination path:", os[1])
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
time.sleep(100)

def job_status(k):
    job = service + "Job/"+k
    r = requests.get(job, headers=headers)
    dictionary = (xmltodict.parse(r.text))
    job_status = dictionary["JobManager_JobListResponse"]["jobs"]["jobSummary"]["@localizedStatus"]
    return job_status

j = job_status(k)
print ("Restoration status:", j)
