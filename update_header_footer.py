import os
import uuid
from shutil import copy

# Support vars
header = ''
footer = ''
footer_started = False
header_started = False
header_ended = False

# First, get the header and footer code from the index.html
with open('index.html') as f:
    for line in f.readlines():
        if not header_started:
            if "<title>" in line:
                header_started = True
        else:
            if not header_ended:
                if 'phx6a' in line:
                    header_ended = True
                else:
                    header += line
            if 'phx6b' in line:
                footer_started = True
            if footer_started:
                footer += line

# Then, create new files for each html file:
bk_dir = './BK_{}'.format(uuid.uuid4())
os.mkdir(bk_dir)
for file_name in os.listdir('.'):

    if file_name.endswith('.html') and file_name != 'index.html':
        
        print('Processing {}'.format(file_name))
        copy(file_name,'{}/{}'.format(bk_dir,file_name))
        
        footer_started = False
        header_ended = False
        header_started = False
        pre_header = ''
        content = '' 
        
        with open(file_name) as f:
            for line in f.readlines():
                
                if not header_started:
                    pre_header += line
                    if "<title>" in line:
                        header_started = True
                else:   
                    if not header_ended:
                        if 'phx6a' in line:
                            header_ended = True
                    if 'phx6b' in line:
                        footer_started = True
                    if header_ended and not footer_started:
                        content += line
        with open(file_name, 'w') as f:
            f.write(pre_header + header + content + footer)










