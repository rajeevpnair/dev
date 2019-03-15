

restore = service + "retrieveToClient"
xml ="""<DM2ContentIndexing_RetrieveToClientReq mode="2" serviceType="1">
<userInfo userGuid=""/>
<header>
<srcContent clientId="" appTypeId="" instanceId="" backupSetId="" subclientId="" fromTime="" toTime=""/>
<destination clientId="" clientName="" inPlace="">
<destPath val=""/>
</destination>
<filePaths val=""/>
<filePaths val=""/>
</header>
<advanced unconditionalOverwrite="" restoreDataAndACL="1" restoreDeletedFiles="1"/>
</DM2ContentIndexing_RetrieveToClientReq>"""

r = requests.get(restore, headers=headers)