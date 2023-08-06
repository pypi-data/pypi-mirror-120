import infapy

infapy.setFileLogger(name="test",level="DEBUG")
infaHandler = infapy.connect()
#v2=infaHandler.v2()
#getActivityDetails = v2.getActivityLog().getAllActivityLog()

v3=infaHandler.v3()
queryString="location=='Prashanth/infapy'"
objectDetails=v3.objects().getObjectID(q=queryString)
# print(objectDetails)
myMTTObject = objectDetails["objects"][1]["id"]
# print(myMTTObject)

objectDependencies = v3.objects().getObjectDependency(objectID=myMTTObject)
print(objectDependencies)


for eachDependenecy in objectDependencies["references"]:
    print()
    print("*****************************************")
    print(eachDependenecy)
    print("*****************************************")
    print()