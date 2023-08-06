
class Infapy():
    def __init__(self,v2,v3,v3SessionID,v3BaseURL,v2BaseURL,v2icSessionID):
        self._v3=v3
        self._v2=v2
        self._v3SessionID = v3SessionID
        self._v3BaseURL = v3BaseURL
        self._v2BaseURL = v2BaseURL
        self._v2icSessionID = v2icSessionID
        
        
    def cdi(self):
        from infapy.cdi import CDI
        return CDI(self._v3,self._v2,self._v2BaseURL,self._v3BaseURL,self._v3SessionID,self._v2icSessionID)
    
    def v2(self):
        from infapy.v2 import V2
        return V2(self._v2,self._v2BaseURL,self._v2icSessionID)

    def v3(self):
        from infapy.v3 import V3
        return V3(self._v3,self._v3BaseURL,self._v3SessionID)