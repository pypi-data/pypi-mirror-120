# Copyright (c) 2021-Present Prashanth Pradeep https://www.linkedin.com/in/prashanth-pradeep/
# All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish, dis-
# tribute, sublicense, and/or sell copies of the Software, and to permit
# persons to whom the Software is furnished to do so, subject to the fol-
# lowing conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABIL-
# ITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT
# SHALL THE AUTHOR BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.
#

import requests as re
from cryptography.fernet import Fernet
import platform
import os
import logging
from infapy.exceptions import InvalidRegionError, InfapyError, ConfigFileReadError, CredentialFileReadError


sysOS = platform.system()    
if(sysOS=="Linux" or sysOS=="Darwin"):
    infaPath = os.path.expanduser("~") + "/.infa"
    # print(infaPath)
    infaConfig=infaPath + "/config"
    infaCredentials=infaPath + "/credentials"
if(sysOS=="Windows"):
    infaPath=os.environ['USERPROFILE'] + "\.infa"
    # print(infaPath)
    infaConfig=infaPath + "\config"
    infaCredentials=infaPath + "\credentials"


##########################################
# Define the logger
###########################################

class NullHandler(logging.Handler):
    def emit(self, record):
        pass


# print(infaPath)
log = logging.getLogger("infapy")
log.addHandler(NullHandler())
# print(log)


def setFileLogger(name="infapy",filepath=None,level=None,formatString=None):
    filename=""
    global log
    if not formatString:
        formatString='%(asctime)s  %(name)s  %(levelname)s: %(message)s'
    if not level:
        level="INFO"
    if filepath is None:
        filename=os.getcwd() + "/infapy.log"
    else:
        filename=filepath + "/infapy.log"
    logger = logging.getLogger(name)
    # print(level)
    logger.setLevel(level)
    fh = logging.FileHandler(filename)
    fh.setLevel(level)
    formatter = logging.Formatter(formatString)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    log = logger
    # log = logging.getLogger(name)
    log.info("New instance of infapy started from hostname: " + platform.node())
    log.info("Host OS: " + sysOS)
    log.info("INFAPY Root Path: " + infaPath)
    

def setStreamLogger(name="infapy",level=None,formatString=None):
    global log
    if not formatString:
        formatString='%(asctime)s  %(name)s  %(levelname)s: %(message)s'
    if not level:
        level="INFO"
    logger = logging.getLogger(name)
    logger.setLevel(level)
    fh = logging.StreamHandler()
    fh.setLevel(level)
    formatter = logging.Formatter(formatString)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    log = logger
    log.info("New instance of infapy started from hostname: " + platform.node())
    log.info("Host OS: " + sysOS)
    log.info("INFAPY Root Path: " + infaPath)
    

def setLogLevel(loglevel):
    _loglevel=loglevel

def encrypt():
    key=b'Qj8yLC3ohEy6fs3As54PWA3HsMyglrl_9hQqJfF8-74='
    fernet = Fernet(key)
    userName=input("Enter your user name: ")
    password = input("Enter your password: ")
    try:
        encUserNameBytes=fernet.encrypt(userName.encode())
        encPasswordBytes=fernet.encrypt(password.encode())
    except Exception as e:
        log.exception(e)
        raise
    
    encUserNameStr=str(encUserNameBytes).strip('b\'')
    encPasswordNameStr=str(encPasswordBytes).strip('b\'')
    
    print("infa_access_key_id: " + encUserNameStr)
    print("infa_secret_access_key: " + encPasswordNameStr)
    
def decrypt(encMessage):
    key=b'Qj8yLC3ohEy6fs3As54PWA3HsMyglrl_9hQqJfF8-74='
    fernet = Fernet(key)
    try:
        encMessage=encMessage.encode()
        decryptedMessage=fernet.decrypt(encMessage).decode()
    except Exception as e:
        log.exception(e)
        raise
    # print("decrypted string: " + decryptedMessage)  
    return decryptedMessage

def readConfigFiles(infaConfig,infaCredentials, profileString):
    userProfile={}
    try:
        with open(infaConfig, "r+") as infaConfigObject:
                lines = infaConfigObject.readlines()
                for i in range(0,len(lines)):
                    line=lines[i]
                    if profileString in line:
                        # print(line)    
                        emptyLineFlag=False
                        while not emptyLineFlag:
                            i=i+1
                            if (i==len(lines)):
                                break

                            nextLine=lines[i]
                            # print(str(i) + " : " + nextLine)
                            if (nextLine in ['\n','\r\n']):
                                emptyLineFlag=True
                                # print("hurray")
                                break
                            # print(type(nextLine))
                            key = nextLine.split(" = ")[0].strip()
                            value = nextLine.split(" = ")[1].strip()
                            # print(key)
                            # print(value)
                            userProfile[key] = value
    except Exception as e:
        log.exception(e)
        raise ConfigFileReadError
        log.exception()
    
    try:    
        with open(infaCredentials, "r+") as infaCredentialsObject:
            lines = infaCredentialsObject.readlines()
            for i in range(0,len(lines)):
                line=lines[i]    
                # print(line)    

                if profileString in line:
                    # print(line)    

                    emptyLineFlag=False
                    
                    while not emptyLineFlag:
                        i=i+1
                        if (i==len(lines)):
                            break

                        nextLine=lines[i]
                        # print(nextLine)
                        if (nextLine in ['\n','\r\n']):
                            emptyLineFlag=True
                            # print("hurray")
                            break
                        key = nextLine.split(" = ")[0].strip()
                        value = nextLine.split(" = ")[1].strip()
                        # print(key)
                        # print(value)
                        userProfile[key] = value
    except Exception as e:
        log.exception(e)
        raise CredentialFileReadError 
    return userProfile
    
       
def connect(profile='default'):
    connectProfile="[" + profile + "]"
    userProfile = readConfigFiles(infaConfig=infaConfig,infaCredentials=infaCredentials,profileString=connectProfile)
    
    userName=decrypt(userProfile["infa_access_key_id"])
    password=decrypt(userProfile["infa_secret_access_key"])
    region=userProfile["region"]
    
    log.debug("User Profile: " + str(userProfile))
    try:
        if(region not in ["us","em","ap"]):
            # log.error("Invalid region provided. Valid regions are us, em or ap")
            raise InvalidRegionError(region)
    except Exception as e:
        log.exception("Got an exception with infapy config file")
        raise
        
        # log.exception(e)
    
    urlV3="https://dm-" + region + ".informaticacloud.com/saas/public/core/v3/login"
    urlV2="https://dm-" + region + ".informaticacloud.com/ma/api/v2/user/login"
    headers = {'Content-Type': "application/json", 'Accept': "application/json"}
    bodyV3={"username": userName,"password": password}
    bodyV2={"@type":"login","username": userName,"password": password}
    try:
        r3 = re.post(url=urlV3, json=bodyV3, headers=headers)
        r2 = re.post(url=urlV2, json=bodyV2, headers=headers)
        
        dataV3 = r3.json()
        dataV2 = r2.json()
        
    except Exception as e:
        log.exception(e)
        raise

    try:
        v3SessionID=dataV3["userInfo"]["sessionId"]
        v3BaseURL=dataV3["products"][0]["baseApiUrl"]
        v2BaseURL=dataV2["serverUrl"]
        v2icSessionID=dataV2["icSessionId"]
    except Exception as e:
        log.exception(e)
        log.error(dataV3)
        log.error(dataV2)
        raise

    log.debug("Connected to Informatica Cloud V3: " + str(dataV3))
    log.debug("Connected to Informatica Cloud V2: " + str(dataV2))
    from infapy.connections import Infapy
    try:
        connObj = Infapy(v2=dataV2,v3=dataV3,v3SessionID=v3SessionID,v3BaseURL=v3BaseURL,v2BaseURL=v2BaseURL,v2icSessionID=v2icSessionID)
    except Exception as e:
        log.exception(e)
        raise
    return connObj






      

        


