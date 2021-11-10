
# Recycle file walking system to try and generate functional skills site


######################



import os
base_path = '/Users/Nick/Documents/GitHub/functional-skills/content'
course_parts = []

# first find all content files
arr = os.listdir(base_path)
print(arr)
# checking this it is locating the entire directory for this repo



# next to use  pre written file structure to start generating the main page
for part in arr:
    sections = os.listdir( f'{base_path}/{part}')
    print(sections)
    for section in sections:
        page_name = f"{part}_{section}_lessons.html"
        with open(page_name,'w') as f:
            f.write('<!DOCTYPE html>\n<html lang ="en">\n<link href="fs_styles.css" type= "text/css" rel="stylesheet"/>\n<!--comment -->\n\n\n')
            f.write(f'<head>\n <title>{part}{section} lessons </title>\n </head> \n<body>\n<hr>\n\n')

            # now lesson page has been established find resource types.

            # find videos and load them
             
            # find and add pdfs to a table


    

   

#then start walking through the 



