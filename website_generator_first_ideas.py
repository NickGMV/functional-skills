
# Recycle file walking system to try and generate functional skills site




######################

import pandas as pd
import os
base_path = '/Users/Nick/Documents/GitHub/functional-skills/content'
#course_parts = []

# first find all content files
arr = os.listdir(base_path)
print(arr)
# checking this it is locating the entire directory for this repo



# next to use  pre written file structure to start generating the main page
for part in arr:
    part_name = f'{part}.html'
    sections = os.listdir( f'{base_path}/{part}')
    print(sections)
    with open(part_name, "w") as g:
        g.write('<!DOCTYPE html>\n<html lang ="en">\n<link href="fs_styles.css" type= "text/css" rel="stylesheet"/>\n<!--comment -->\n\n\n')
        g.write(f'<head>\n <title>{part} lessons </title>\n</head> \n<body>\n<hr>\n\n')
        g.write('<div class = "buffer"></div>\n\n')
        g.write(f'<a href = "./{part}.html"> go back a level </a>')
        for section in sections:
            g.write(f'<a href = "./{part}_{section}_lessons.html"> go to lesson page </a>')

    #this loop will be refactored but for now it will iterate through the sections and buid each lesson page
    for section in sections:
        page_name = f"{part}_{section}_lessons.html"

        #writing the opening html code for a lesson page
        with open(page_name,'w') as f:
            f.write('<!DOCTYPE html>\n<html lang ="en">\n<link href="fs_styles.css" type= "text/css" rel="stylesheet"/>\n<!--comment -->\n\n\n')
            f.write(f'<head>\n <title>{part}{section} lessons </title>\n</head> \n<body>\n<hr>\n\n')
            f.write('<div class = "buffer"></div>\n\n')
            f.write(f'<a href = "./{part}"> go back a level </a>')


            # now lesson page has been established find resource types.
            
            # find videos and load them
            try:
                structure = os.listdir(f'{base_path}/{part}/{section}/instructionsections')
                print(f'found session structure for {part}{section}')
                #print(structure)
                structure = [file for file in structure if file.endswith('csv') ]
                #print(structure)
                lesson = pd.read_csv(f'{base_path}/{part}/{section}/instructionsections/{structure[0]}')
                print('pandas worked')
                for index, row in lesson.iterrows():
                    print('df loaded')
                    if row['type'] == 'heading':
                        f.write(f'<h2>{row["content"]}</h2>')

                    elif row['type'] == 'text':
                        f.write(f'<p>{row["content"]}</p>')
#<div style="position: relative; padding-bottom: 56.25%; height: 0;"><iframe src="https://www.loom.com/embed/de00a87a28864b7784607282e65f40dd" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe>
                    elif row['type']== 'vid':
                        f.write(f'<iframe src = {row["content"]} webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe>')

                    else:
                        print('content type not recognised check your planning document for errors')
            except:
                print('there appears to be no planning doc for this section')


             
            # find pdfs of exercises

            f.write(f'<h2> Practice your skills using our exercises</h2>')
            try:
                pdf_path = f'{base_path}/{part}/{section}/pdfs'
                # content\part_1\section_1\exercises\T01 Class Ex - Directed Numbers.pdf
                print(f'pdfs are stored in {pdf_path}')
                #pp = os.listdir(f'{base_path}/{section}')
                pp = os.listdir(f'{base_path}/{part}/{section}/pdfs')
                print(pp)
                for pdf in pp:
                    print(pdf)
                    f.write(f'<iframe class="pdf coached" src="./content/{part}/{section}/pdfs/{pdf}"  type="application/pdf" allow="fullscreen"></iframe>\n')
                #for pdf in pdfs:
                #f.write(f'<embed class="pdf coached" src="{pdf}" type="application/pdf">')
            except:
                print(f'no exercises folder present in {section}')

            #find pdfs of exams


            f.write(f'<h2> Get exam ready with exam practice </h2>')
            try:
                pdf_path = f'{base_path}/{part}/{section}/examqs'
                # content\part_1\section_1\exercises\T01 Class Ex - Directed Numbers.pdf
                print(f'pdfs are stored in {pdf_path}')
                #pp = os.listdir(f'{base_path}/{section}')
                pp = os.listdir(f'{base_path}/{part}/{section}/examqs')
                print(pp)
                for pdf in pp:
                    print(pdf)
                    f.write(f'<iframe class="pdf coached" src="./content/{part}/{section}/examqs/{pdf}"  type="application/pdf" allow="fullscreen"></iframe>\n')
                #for pdf in pdfs:
                #f.write(f'<embed class="pdf coached" src="{pdf}" type="application/pdf">')
            except:
                print(f'no exam folder present in {section}')

#then start walking through the 



