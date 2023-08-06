import sys
import os
print(f"Can't import,you can found this path:'{sys.executable[:-10]}Lib\\site-pakages\\downloader-python\\main.py',and then,use python to run it.")
print(os.system(f'{sys.executable} {sys.executable[:-10]}Lib\\site-pakages\\downloader-python\\main.py'))
