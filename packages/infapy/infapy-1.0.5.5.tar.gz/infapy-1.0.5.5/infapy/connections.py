import infapy

class Infapy():
    """infapy is the main class with 
    which you can easily use the IICS Rest APIs
    """
    def __init__(self,v2,v3,v3SessionID,v3BaseURL,v2BaseURL,v2icSessionID):
        """Arguments required for initializing the infapy class

        Args:
            v2 [json response] : v2 login API response
            v3 [json response] : v3 login API Response
            v3SessionID [String] : Session ID from the v3 response
            v3BaseURL [String] : v3 base url
            v2BaseURL [String] : v2 base url
            v2icSessionID [String] : v2 session ID
        """
        self._v3=v3
        self._v2=v2
        self._v3SessionID = v3SessionID
        self._v3BaseURL = v3BaseURL
        self._v2BaseURL = v2BaseURL
        self._v2icSessionID = v2icSessionID
        
        
    def cdi(self):
        """cdi handler to access the IICS cdi APIs 

        Returns:
            Class Object : infapy.cdi.CDI
        """
        from infapy.cdi import CDI
        infapy.log.info("Created the cdi object to access the iics cdi apis")
        return CDI(self._v3,self._v2,self._v2BaseURL,self._v3BaseURL,self._v3SessionID,self._v2icSessionID)
    
    def v2(self):
        """v2 handler to access all IICS V2 APIs

        Returns:
            Class Object: infapy.v2.V2
        """
        from infapy.v2 import V2
        infapy.log.info("Created the v2 object to access the iics v2 apis")
        return V2(self._v2,self._v2BaseURL,self._v2icSessionID)

    def v3(self):
        """v3 handler to access all the IICS V3 APIs

        Returns:
            Class object : infapy.v3.V3
        """
        from infapy.v3 import V3
        infapy.log.info("Created the v3 object to access the iics v3 apis")
        return V3(self._v3,self._v3BaseURL,self._v3SessionID)

    
    def getLoginDetails(self):
        """getLoginDetails is a method to
        get the login details.

        Returns:
            infaLoginDetails[list]: v2 and v3 login details
        """
        loginDetails = [self._v2, self._v3]
        return loginDetails