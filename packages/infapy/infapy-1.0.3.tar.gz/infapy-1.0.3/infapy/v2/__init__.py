import requests as re
import infapy

class V2():
    def __init__(self,v2,v2BaseURL,v2icSessionID):
        print("Created V2 Class")
        self._v2=v2
        self._v2BaseURL = v2BaseURL
        self._v2icSessionID = v2icSessionID
        
    def getAllActivityLog(self):
        url=self._v2BaseURL + "/api/v2/activity/activityLog"
        headers = {'Content-Type': "application/json", 'Accept': "application/json","icSessionID":self._v2icSessionID}
        # The below format is for post
        # bodyV3={"username": userName,"password": password}
        # r3 = re.post(url=urlV3, json=bodyV3, headers=headers)
        try:
            response = re.get(url=url, headers=headers)
        except Exception as e:
            infapy.log.exception(e)
            raise
        data = response.json()
        return data
