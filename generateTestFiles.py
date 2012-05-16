import random
import os
import time

if not os.path.exists("test_files/"):
    os.mkdir("test_files/")
    
for i in xrange(20):
    if (random.randint(0, 100) % 4) >= 1:
        filename = '%#05d.bak' % (random.randint(10000, 99999))
    else:
        filename = '%#05d.trn' % (random.randint(10000, 99999))
    f = open('test_files/%s' % filename, 'w')
    f.write('')
    f.close()
    time.sleep(0.1)
