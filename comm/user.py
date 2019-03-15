import requests
import sys
import xml.etree.ElementTree as ET
from xml.etree import ElementTree
import random
import xmltodict
import json

from random import randint

import base64
import json
global b

service = 'http://104.211.205.144/webconsole/api/'

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
   print (r.status_code)
headers = {'Authtoken': token, 'Content-Type': 'application/xml'} 

get_user = service + "user"
r = requests.get(get_user, headers=headers)
print (r.status_code)
print (r.text)
#userGUID="4C1C8327-233F-46F5-910B-E873FBEBE494"

 
