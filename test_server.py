import xmlrpclib
s = xmlrpclib.ServerProxy('http://127.0.0.1:60010')
#print s.system.listM
print s.test_rpc()
print s.parseThis([" and view amazing and also the ambience was nice","staff friendly and faicilities incredible"],["staff not so friendly","view not so good"])
#print s.min(10,4)