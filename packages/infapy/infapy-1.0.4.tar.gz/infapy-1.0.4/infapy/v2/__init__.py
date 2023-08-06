import requests as re
import infapy

class V2():
    def __init__(self,v2,v2BaseURL,v2icSessionID):
        """This class is used to leverage the IICS V2 APIs

        Args:
            v2 (json): login response of v2 login API
            v2BaseURL (string): The base url which we get from the v2 login API
            v2icSessionID (string): The icSessionID from the v2 Login API
        """
        infapy.log.info("created a v2 class object successfully")
        infapy.log.info("v2BaseURL: " + v2BaseURL)
        self._v2=v2
        self._v2BaseURL = v2BaseURL
        self._v2icSessionID = v2icSessionID
        
    def getActivityLog(self):
        """This function returns an object of getActivityLog
        which has multiple sub methods to fetch the activity log

        Returns:
            class object: v2.getActivityLog.GetActivityLog
        """
        from infapy.v2.getActivityLog import GetActivityLog
        return GetActivityLog(self._v2,self._v2BaseURL,self._v2icSessionID)