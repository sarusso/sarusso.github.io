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
root_bk_dir = './BK_{}'.format(uuid.uuid4())
os.mkdir(root_bk_dir)
dirs = ['.', 'blog']
for dir in dirs:
    if dir != '.':
        os.mkdir('{}/{}'.format(root_bk_dir, dir))
    for file_name in os.listdir(dir):
    
        if file_name.endswith('.html') and file_name != 'index.html':
            
            print('Processing {}/{}'.format(dir,file_name))
            copy('{}/{}'.format(dir,file_name),'{}/{}/{}'.format(root_bk_dir,dir,file_name))
            
            footer_started = False
            header_ended = False
            header_started = False
            pre_header = ''
            content = '' 
            
            with open('{}/{}'.format(dir,file_name)) as f:
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
            with open('{}/{}'.format(dir,file_name), 'w') as f:
                if dir != '.':
                    this_header = header.replace('./', '../')
                    this_footer = footer.replace('./', '../')
                else:
                    this_header = header
                    this_footer = footer
                
                f.write(pre_header + this_header + content + this_footer)










