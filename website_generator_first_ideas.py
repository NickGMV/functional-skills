
# Recycle file walking system to try and generate functional skills site

issue_count = 0
######################
def banners(banner1,banner2,webpage):
    
        
    h = open(webpage,'a')
    f = open(banner1 ,'r')
    g = open(banner2, 'r')
        
    for line in f:
        #print(line)
        h.write(line)
    #h.close()

    #h= open(webpage,'w')

    for line in g:
        h.write(line)
    
    h.close()
    f.close()
    g.close()

def initsession():
    e = open('error.txt','a')
    time = datetime.now()
    e.write('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n')
    e.write('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n')
    e.write(f'New session started at -- {time} \n\n')
    e.write('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n')
    e.write('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n\n')

    f = open('success.txt','a')
    f.write('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n')
    f.write('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n')
    f.write(f'New session started at -- {time} \n\n')
    f.write('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n')
    f.write('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n\n')

def report_issue(x):
    #send reports to a txt file  in the root directory
    e = open('error.txt','a')
    time = datetime.now()
    e.write(f'reported error at {time}\n')
    e.write(f'{x}\n\n')
    global issue_count 
    issue_count +=1


def report_success(x):
    #send reports to a txt file  in the root directory
    e = open('success.txt','a')
    time = datetime.now()
    e.write(f'process successful at {time}\n')
    e.write(f'{x}\n\n')



import pandas as pd
import os
import shutil
import openpyxl
from datetime import datetime

# find the content folders from which to generate the site

base_path = './content'


#create a universal parent directory for all generated content
# Directory
initsession()

try:
    main_directory = "Functional skills maths"
    # Parent Directory path
    parent_directory = "./"
    # Path
    path = os.path.join(parent_directory, main_directory)
    #Create the directory
    os.mkdir(path)
except:
    # re-add input for confirmation after development is finished
    go_ahead = 'the content directory has already been converted to a website! \n \
    if you wish to over write this version enter any key execpt "n"'
    if(go_ahead.lower() != 'n'):
        #delete current site design to replace it
        try:
            shutil.rmtree(path)
        except OSError as e:
            print("Error: %s - %s." % (e.filename, e.strerror))
            report_issue(" issue with file readers report to developer")

        main_directory = "Functional skills maths"
        # Parent Directory path
        parent_directory = "./"
        # Path
        path = os.path.join(parent_directory, main_directory)
        #Create the directory
        os.mkdir(path)

    else:
        # terminate and produce an error report
        report_issue('some error with folder creation for website CONSULT with tech team.')

#copy style and js resources so that they can be used by all pages.


original = './fs_styles.css'
target = f'{path}/fs_styles.css'

shutil.copyfile(original, target)


#find all the sub-parts (content sections/courses) load all parts and generate navigation pages
level1 = os.listdir(base_path)
report_success(f' content at the first level is {level1}\n\n\n')

main_page_path = f"{parent_directory}/{main_directory}/main_page.html"
with open(main_page_path ,"w") as h:
    
    # h refers to the main nav page being written by python in this loop
    h.write('<!DOCTYPE html>\n<html lang ="en">\n<link href="./fs_styles.css" type= "text/css" rel="stylesheet"/>\n<!--comment -->\n\n\n')
    h.write(f'<head>\n <title>main_page </title>\n</head> \n<body>\n<hr>\n\n')
    h.write('<div class = "buffer"></div>\n\n')
    
    

    for part in level1:
        h.write(f'<a href = "./{part}/{part}.html"> go to {part} </a>')
        os.mkdir(f'./{main_directory}/{part}')
        report_success(f'{part} was found and added to the site build')

banners('banner1.txt','banner2.txt',main_page_path)

# checking this it is locating the entire directory for this repo



# generate actual lesson content now navigation pages are completed
for part in level1:
    part_name = f'{part}.html'
    #print(part)
    sections = os.listdir( f'{base_path}/{part}')
    report_success(f' sections in {part} are {sections} they will be added to site')


    with open(f'./{main_directory}/{part}/{part_name}', "w") as g:
        g.write('<!DOCTYPE html>\n<html lang ="en">\n<link href="../fs_styles.css" type= "text/css" rel="stylesheet"/>\n<!--comment -->\n\n\n')
        g.write(f'<head>\n <title>{part} lessons </title>\n</head> \n<body>\n<hr>\n\n')
        g.write('<div class = "buffer"></div>\n\n')
        g.write(f'<a href = "../main_page.html"> go back to main page </a>')
        for section in sections:
            g.write(f'<a href = "./{part}_{section}_lessons.html"> go to lesson {part} {section} </a>')

    #this loop will be refactored but for now it will iterate through the sections and build each lesson page
    for section in sections:
        page_name = f"./{main_directory}/{part}/{part}_{section}_lessons.html"

        #writing the opening html code for a lesson page
        with open(page_name,'w') as f:
            f.write(f'<!DOCTYPE html>\n<html lang ="en">\n<link href="../fs_styles.css" type= "text/css" rel="stylesheet"/>\n<!--comment -->\n\n\n')
            f.write(f'<head>\n <title>{part}{section} lessons </title>\n</head> \n<body>\n<hr>\n\n')
            f.write('<div class = "buffer"></div>\n\n')
            f.write(f'<a href = "./{part}.html"> go back a level </a>')


            # now lesson page has been established find resource types.
            
            # find page plans and generate pages
            try:
                structure = os.listdir(f'{base_path}/{part}/{section}/instructionsections')
                report_success(f'found session structure for {part}{section}')
                #print(structure)
                structure = [file for file in structure if file.endswith('xlsx') ]
                #print(structure)
                location = f'{base_path}/{part}/{section}/instructionsections/{structure[0]}'
                report_success(f'planning doc is located at {location}')
                lesson = pd.read_excel(f'{base_path}/{part}/{section}/instructionsections/{structure[0]}')
                #lesson.dropna()
                #print('pandas worked')
                for index, row in lesson.iterrows():
                    #print(str(row['Content']).lower())
                    if row['Type'] == 'heading' and str(row['Content']).lower() !='nan':
                        #print(row['Content'])
                        f.write(f'<h2>{row["Content"]}</h2>')

                    elif row['Type'] == 'paragraph'  and str(row['Content']).lower() !='nan':
                        #print(row['Content'])
                        f.write(f'<p>{row["Content"]}</p>')
#<div style="position: relative; padding-bottom: 56.25%; height: 0;"><iframe src="https://www.loom.com/embed/de00a87a28864b7784607282e65f40dd" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe>
                    elif row['Type']== 'video'  and str(row['Content']).lower() !='nan':
                        #print(row['Content'])
                        f.write(f'<iframe class = "vid" src = {row["Content"]} webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe>')

                    else:
                        report_issue(f'content type not recognised check your planning document for errors - find it at {location}')
            except:
                report_issue(f'There is an error with a planning doc check in {location} if there should be content for this section')
                #lesson = pd.read_excel(f'{base_path}/{part}/{section}/instructionsections/{structure[0]}')

             
            # find pdfs of exercises

            
            try:
                pdf_path = f'{base_path}/{part}/{section}/pdfs'
                # content\part_1\section_1\exercises\T01 Class Ex - Directed Numbers.pdf
                report_success(f'pdfs were found in {pdf_path}')
                #pp = os.listdir(f'{base_path}/{section}')
                pp = os.listdir(f'{base_path}/{part}/{section}/pdfs')
                if pp:
                    f.write(f'<h2> Practice your skills using our exercises</h2>')
                    #print(pp)
                    for pdf in pp:
                        print(pdf)
                        f.write(f'<iframe class="pdf coached" src="../../content/{part}/{section}/pdfs/{pdf}"  type="application/pdf" allow="fullscreen"></iframe>\n')
                    #for pdf in pdfs:
                #f.write(f'<embed class="pdf coached" src="{pdf}" type="application/pdf">')
            except:
                report_issue(f'no pdf exercises folder present in {pdf_path} check if this is needed')

            #find pdfs of exams


            #f.write(f'<h2> Get exam ready with exam practice </h2>')
            try:
                pdf_path = f'{base_path}/{part}/{section}/examqs'
                # content\part_1\section_1\exercises\T01 Class Ex - Directed Numbers.pdf
                report_success(f'exam pdfs were found in {pdf_path}')
                #pp = os.listdir(f'{base_path}/{section}')
                pp = os.listdir(f'{base_path}/{part}/{section}/examqs')
                if pp:
                    f.write(f'<h2> Get exam ready with exam practice </h2>')
                    #print(pp)
                    for pdf in pp:
                        #print(pdf)
                        f.write(f'<iframe class="pdf coached" src="../../content/{part}/{section}/examqs/{pdf}"  type="application/pdf" allow="fullscreen"></iframe>\n')
                #for pdf in pdfs:
                #f.write(f'<embed class="pdf coached" src="{pdf}" type="application/pdf">')
            except:
                report_issue(f'no exam folder present in {pdf_path}')

print(f'full process ran with {issue_count} reports in error report' )



