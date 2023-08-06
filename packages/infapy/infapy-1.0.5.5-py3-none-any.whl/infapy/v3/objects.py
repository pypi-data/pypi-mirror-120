import requests as re
import infapy
from infapy.exceptions import LimitExceededError

class Objects():
    def __init__(self,v3,v3BaseURL,v3SessionID):
        self._v3 = v3
        self._v3BaseURL = v3BaseURL
        self._v3SessionID = v3SessionID
      

    def getObjectID(self,q=None,limit=200,skip=None):
        """get the object IDs of objects in IICS

        Args:
            q ([type], optional): [description]. Defaults to None.
            limit (int, optional): [description]. Defaults to 200.
            skip ([type], optional): [description]. Defaults to None.
        """
        infapy.log.info("getObjectID Method called. Processing request....")
        try:
            if limit > 200:
                infapy.log.error("Error while building the getObjectID API")
                infapy.log.error("Limit provided exceeds max allowed of 200")
                raise LimitExceededError(limit)
        except Exception as e:
            infapy.log.exception(e)
            raise

        queryString=""
        queryStringFlag=True
        if q:
            queryString = queryString + "q=" + q
        else:
            print("Test")
            queryStringFlag=False

        limitString="limit=" + str(limit)

        skipString=""
        skipStringFlag=True
        if skip:
            skipString = skipString + "skip=" + str(skip)
        else:
            skipStringFlag=False
            
        urlQuery=""
        if(queryStringFlag):
            urlQuery = urlQuery + queryString
            urlQuery=urlQuery+"&"+limitString
        else:
            urlQuery=limitString
        

        if(skipStringFlag):
            urlQuery=urlQuery+"&"+skipString

        url=self._v3BaseURL + "/public/core/v3/objects?" + urlQuery
        headers = {'Content-Type': "application/json", 'Accept': "application/json","INFA-SESSION-ID":self._v3SessionID}
        infapy.log.info("get object URL - " + url)
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
        infapy.log.info("Fetched the all the object details from IICS")
        data = response.json()
        infapy.log.info("getObjectID Method call completed. Processing completed")
        return data

        
    def getObjectDependency(self,objectID,refType="uses",limit=50,skip=0):
        """Get object dependency of objects in IICS

        Args:
            objectID ([type]): [description]
            refType (str, optional): uses or usedBy. Defaults to "uses".
            limit (int, optional): Max 50. Defaults to 50.
            skip ([type], optional): Number of elements to skip from the beginning. Defaults to 0.

        Returns:
            list of dict: dependency list in json
        """
        infapy.log.info("getObjectDependency Method called. Processing request....")
        try:
            if limit > 50:
                infapy.log.error("Error while building the getObjectDependency API")
                infapy.log.error("Limit provided exceeds max allowed of 50")
                raise LimitExceededError(limit)
        except Exception as e:
            infapy.log.exception(e)
            raise


        urlQuery="refType="+refType+"&skip="+str(skip)+"&limit="+str(limit)
        url=self._v3BaseURL + "/public/core/v3/objects/" + objectID + "/references?" + urlQuery
        headers = {'Content-Type': "application/json", 'Accept': "application/json","INFA-SESSION-ID":self._v3SessionID}
        infapy.log.info("get object dependency URL - " + url)
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
        infapy.log.info("Fetched the object dependencies from IICS")
        data = response.json()
        infapy.log.info("getObjectID Method call completed. Processing completed")
        return data

        