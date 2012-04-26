import xmlrpclib
s = xmlrpclib.ServerProxy('http://localhost:8000')
print s.parseThis(['Review 1 pos, Review 2 pos'],['Review 1 neg','Review 2 neg'])