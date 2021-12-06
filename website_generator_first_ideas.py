
# Recycle file walking system to try and generate functional skills site




######################
#import numpy




import numpy as np
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
    sections = os.listdir( f'{base_path}/{part}')
    print(sections)
    for section in sections:
        page_name = f"{part}_{section}_lessons.html"
        with open(page_name,'w') as f:
            f.write('<!DOCTYPE html>\n<html lang ="en">\n<link href="fs_styles.css" type= "text/css" rel="stylesheet"/>\n<!--comment -->\n\n\n')
            f.write(f'<head>\n <title>{part}{section} lessons </title>\n</head> \n<body>\n<hr>\n\n')

            # now lesson page has been established find resource types.
            
            # find videos and load them
            try:
                structure = os.listdir(f'{base_path}/{part}/{section}/instruction sections')
                print(f'found session structure for {part}{section}')
                lesson = pd.read_csv(structure)
                for row in lesson[['type','content']]:
                    if row['type'] == 'heading':
                        f.write(f'<h2>{row["content"]}</h2>')
                    elif row['type'] == 'text':
                        f.write(f'<p>{row["content"]}</p>')
                    elif row['type']== 'vid':
                        f.write(f'<iframe src = {row["content"]}></iframe>')
                    else:
                        print('content type npt recognised check your planning document for errors')
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



