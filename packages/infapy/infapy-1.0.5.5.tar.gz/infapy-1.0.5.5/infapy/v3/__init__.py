import requests as re
import infapy

# infapy.log = logging.getinfapy.log(__name__)

class V3():
    """V3 class is a wrapper class for all the IICS rest v2 APIs
    """
    def __init__(self,v3,v3BaseURL,v3SessionID):
        """This class is used to leverage the IICS V2 APIs

        Args:
            v3 (json): login response of v23 login API
            v3BaseURL (string): The base url which we get from the v3 login API
            v3SessionID (string): The SessionID from the v3 Login API
        """
        infapy.log.info("created a v2 handler object successfully")
        infapy.log.info("v3BaseURL: " + v3BaseURL)
        self._v3=v3
        self._v3SessionID = v3SessionID
        self._v3BaseURL = v3BaseURL
        
    def objects(self):
        from infapy.v3.objects import Objects
        return Objects(v3=self._v3,v3BaseURL=self._v3BaseURL,v3SessionID=self._v3SessionID)