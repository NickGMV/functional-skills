
# Recycle file walking system to try and generate functional skills site




######################



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
            f.write(f'<head>\n <title>{part}{section} lessons </title>\n </head> \n<body>\n<hr>\n\n')

            # now lesson page has been established find resource types.

            # find videos and load them
             
            # find and add pdfs to a table
            try:
                pdf_path = f'{base_path}/{section}/ex'
                # content\part_1\section_1\exercises\T01 Class Ex - Directed Numbers.pdf
                print(f'pdfs are stored in {pdf_path}')
                pdfs = os.listdir(pdf_path)
                print(pdfs)
                #for pdf in pdfs:
                    #f.write(f'<embed class="pdf coached" src="{pdf}" type="application/pdf">')
            except:
                print(f'no exercises folder present in {section}')

   

#then start walking through the 



