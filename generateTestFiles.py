import random
import os

if not os.path.exists("test_files/"):
    os.mkdir("test_files/")
for i in xrange(30):
    filename = '%#05d.bak' % (random.randint(10000, 99999))
    f = open('test_files/%s' % filename, 'w')
    f.write('')
    f.close()
    
