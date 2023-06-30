import os
if os.path.exists('/stage/models/sciner-scibert/config.json'):
    print('success')
else:
    raise OSError("/stage/models/sciner-scibert/config.json does not exist")