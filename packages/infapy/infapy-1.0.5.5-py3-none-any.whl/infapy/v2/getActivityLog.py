import logging
import requests as re
import infapy
import json

# infapy.log = logging.getinfapy.log(__name__)
# print(infapy.log)
class GetActivityLog:
    """This class is a handler for fetching
    the Activity Log from IICS
    """
    def __init__(self,v2,v2BaseURL,v2icSessionID):
        self._v2 = v2
        self._v2BaseURL = v2BaseURL
        self._v2icSessionID = v2icSessionID
        

    def getAllActivityLog(self):
        """getAllAcitivityLog returns all the activity logs from IICS in dict format

        Returns:
            List of dict: <Acticity Log in dict Format>
        """
        url=self._v2BaseURL + "/api/v2/activity/activityLog"
        headers = {'Content-Type': "application/json", 'Accept': "application/json","icSessionID":self._v2icSessionID}
        infapy.log.info("GetAllActivityLog URL - " + url)
        infapy.log.info("API Headers: " + str(headers))
        infapy.log.info("Body: " + "This API requires no body")
        # The below format is for post
        # bodyV3={"username": userName,"password": password}
        # r3 = re.post(url=urlV3, json=bodyV3, headers=headers)
        try:
            response = re.get(url=url, headers=headers)
            infapy.log.debug(str(response.json()))
        except Exception as e:
            infapy.log.exception(e)
            raise
        infapy.log.info("Fetched the all the Activity log from IICS")
        data = response.json()
        return data

        