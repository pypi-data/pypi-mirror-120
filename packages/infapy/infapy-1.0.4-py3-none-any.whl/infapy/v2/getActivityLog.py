import infapy

class GetActivityLog:
    def __init__(self,v2,v2BaseURL,v2icSessionID):
        self._v2 = v2
        self._v2BaseURL = v2BaseURL
        self._v2icSessionID = v2icSessionID
        

    def getAllActivityLog(self):
        """getAllAcitivityLog returns all the activity logs from IICS in json format

        Returns:
            json: <Acticity Log in Json Format>
        """
        url=self._v2BaseURL + "/api/v2/activity/activityLog"
        headers = {'Content-Type': "application/json", 'Accept': "application/json","icSessionID":self._v2icSessionID}
        infapy.log.info("GetAllActivityLog URL - " + url)
        infapy.log.info("API Headers: " + headers)
        infapy.log.info("Body: " + "This API requires no body")
        # The below format is for post
        # bodyV3={"username": userName,"password": password}
        # r3 = re.post(url=urlV3, json=bodyV3, headers=headers)
        try:
            response = re.get(url=url, headers=headers)
            infapy.log.debug(response)
        except Exception as e:
            infapy.log.exception(e)
            raise
        data = response.json()
        return data

        