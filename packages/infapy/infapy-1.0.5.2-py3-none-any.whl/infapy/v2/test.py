import infapy

infapy.setFileLogger(name="test",level="DEBUG")
infaHandler = infapy.connect()
v2=infaHandler.v2()
getActivityDetails = v2.getActivityLog().getAllActivityLog()