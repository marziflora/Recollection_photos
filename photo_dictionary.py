#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import json
from PIL import Image

path = 'A:/Zdjęcia'

for directory, subdirectories, files in os.walk(path):
    for file in files:
        if file.endswith(".jpg"):
            nr_files +=1 
            path_file = f'{directory}/{file}'.replace("\\", "/")
            try:
                exif_date = Image.open(path_file)._getexif()[306]
                dictionary[path_file] = exif_date[:10]
            except:
                pass
#                 print("Nie udało się pozyskać informacji o utworzeniu:", path_file)

print("Zidentyfikowano ", nr_files, " zdjęć")
print("Data wykonania istniała dla: ", len(dictionary), "zdjęć")
file = open("slownik_zdjec.json", "w")
json.dump(dictionary, file)
file.close()
print("Zapisano slownik zdjec")


# In[ ]:




