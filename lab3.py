import re
import datetime
import os
import pandas as pd
import hashlib
import magic
import mimetypes
import time

# specify the directory path where the files are located
dir_path = 'E:'

# create an empty list to store the file names...
file_names = []
extensions = []
md5s=[]
sha1s=[]
sha256s=[]
magic_numbers=[]
extension_matches=[]
creation_times=[]
modification_times=[]
access_times=[]

f= magic.Magic(uncompress=True,mime=True)

# iterate through all files in the directory
for file in os.listdir(dir_path):
    # check if the file is a regular file (i.e., not a directory)
    if os.path.isfile(os.path.join(dir_path, file)):
        # if so, add the file name to the list
        name,extension=os.path.splitext(file)
        file_names.append(name)
        extensions.append(extension)
        md5s.append(hashlib.md5(file.encode('utf-8')).hexdigest()) 
        sha1s.append(hashlib.sha1(file.encode('utf-8')).hexdigest())
        sha256s.append(hashlib.sha256(file.encode('utf-8')).hexdigest())
        magic_number=f.from_file(os.path.join(dir_path,file))
        magic_numbers.append(magic_number)
        creation_times.append(time.ctime(os.path.getctime(os.path.join(dir_path, file))))
        modification_times.append(time.ctime(os.path.getmtime(os.path.join(dir_path, file))))
        access_times.append(time.ctime(os.path.getatime(os.path.join(dir_path, file))))
        # check if the magic number contains the file extension
        if extension.lower() == '':
            extension_matches.append(False)
        elif mimetypes.guess_type('test'+extension.lower())[0] in magic_number.lower():
            extension_matches.append(True)
        else:
            extension_matches.append(False)

# create a Pandas dataframe with the file names
df = pd.DataFrame(
    {'file_name': file_names, 
     'extension': extensions, 
     'md5': md5s, 
     'sha1': sha1s, 
     'sha256': sha256s, 
     'magic': magic_numbers,
     'Extension_matches': extension_matches,
     'Creation times:':creation_times,
     'Modification times:':modification_times,
     'Access times:':access_times})

# print the dataframe
print(df)

log_path = 'setupapi.dev2.log'
usb_devices_list=[]

with open(log_path, "r") as log_file:
     # Store information about each USB device in a dictionary
     for line in log_file:
        # Find all USB device installation events and extract information about each device2
        obj=re.match(
        r'^>>>  \[Device Install.*#(Disk&Ven_[A-Za-z0-9]+)&(Prod_([\w\s\S]+?))&(Rev_([\w\s\S]+?))#([\w\s\S]+?)#.*\]',
        line,
        )
        if obj:
            vendor_id=obj.group(1)
            product_id=obj.group(2)
            instance_id=obj.group(3)
            serial_number=obj.group(6)
            line=next(log_file)
            event_line=line.split("t")
            event_time=event_line[3]
            usb_devices={
                "vendor_id":vendor_id,
                "product_id":product_id,
                "instance_id":instance_id,
                "event_time":event_time
            }
            usb_devices_list.append(usb_devices)
            for device in usb_devices_list:
                print(device)