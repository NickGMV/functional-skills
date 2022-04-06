import pandas as pd
import glob
import pandas as pd
import os
import shutil
import openpyxl
from datetime import datetime
#from google.colab import drive #activate for google drive version

######################

def initsession():
    e = open('./backgroundfiles/error.txt','a')
    time = datetime.now()
    e.write('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n')
    e.write('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n')
    e.write(f'New session started at -- {time} \n\n')
    e.write('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n')
    e.write('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n\n')

    f = open('./backgroundfiles/success.txt','a')
    f.write('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n')
    f.write('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n')
    f.write(f'New session started at -- {time} \n\n')
    f.write('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n')
    f.write('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n\n')

def report_issue(x):
    #send reports to a txt file  in the root directory
    e = open('./backgroundfiles/error.txt','a')
    time = datetime.now()
    e.write(f'reported error at {time}\n')
    e.write(f'{x}\n\n')
    global issue_count 
    issue_count +=1

def report_success(x):
    #send reports to a txt file  in the root directory
    e = open('./backgroundfiles/success.txt','a')
    time = datetime.now()
    e.write(f'process successful at {time}\n')
    e.write(f'{x}\n\n')

def establish_build():

    global path
    global main_directory
    global parent_directory

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
        go_ahead = 'z'
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
            
def copy_dependencies():
    global path 
    #copy general style sheet to site build
    original = './backgroundfiles/fs_styles.css'
    target = f'{path}/fs_styles.css'
    shutil.copyfile(original, target)
    #copy assets folder to site build
    original_assets = './backgroundfiles/assets'
    target_assets = f'{path}/assets'
    shutil.copytree(original_assets, target_assets)
    #copy additional style sheets for embedded content pages
    original2 = './backgroundfiles/fs_styles_content.css'
    target2 = f'{path}/fs_styles_content.css'
    shutil.copyfile(original2, target2)

# find the content folders from which to generate the site

# key files generated

# h - main page and navigation
# g - landing pages for sessions
# f - session content pages
# b - bios page 
# i - exam qs by topic
# j - videos by topic


base_path = './content'
issue_count=0
path = ""
main_directory =""
parent_directory = ""

#create a universal parent directory for all generated content

#functions for basic set up

#set up folder structure and delete previous version
establish_build()
# copy assets and back ground files
copy_dependencies()
# open up error reporting session
initsession()

######### build static pages bios, maths specs etc
bios_folder = f'{parent_directory}{main_directory}/bios'
bios_path = f'{parent_directory}{main_directory}/bios/bios.html'
os.mkdir(bios_folder)

bio_data = pd.read_excel('./backgroundfiles/assets/bios/bios.xlsx')
with open(bios_path,'w') as b:
    b.write('''
    <!DOCTYPE html>
<html lang ="en">
<link href="../fs_styles.css" type= "text/css" rel="stylesheet"/>
<!--comment -->
<head>
 <title>Maths functional skills - One stop shop </title>
 </head> 
<body>
<div class = "buffer2"></div>
<div class = "content_wrapper">
    ''')
    for index, row in bio_data.iterrows():
         b.write(f'<h2>{row[0]}</h2>')
         b.write(f'<img class = "bio" src="../assets/bios/{row[1]}">')
         b.write(f'<p>{row[2]}</p>')
         b.write(f'<a href = "{row[3]}">{row[3]}</a>')
     







#find all the sub-parts (content sections/courses) load all parts and generate navigation pages
level1 = os.listdir(base_path)
report_success(f' content at the first level is {level1}\n\n\n')

main_page_path = f"{parent_directory}/{main_directory}/main_page.html"
with open(main_page_path ,"w") as h:
    
    # h refers to the main nav page being written by python in this loop
    h.write('<!DOCTYPE html>\n<html lang ="en">\n<link href="./fs_styles.css" type= "text/css" rel="stylesheet"/>\n<!--comment -->\n\n\n')
    h.write(f'<head>\n <title>Maths functional skills - One stop shop </title>\n </head> \n<body>\n\n\n')
    h.write('<div class = "buffer"></div>\n\n')
    h.write('<div class = "content_wrapper">\n')
    h.write('<iframe id = "frame" class = "viewer" src = "message.html" allow="fullscreen">\n')
    h.write('</iframe>\n')
    h.write('</div>\n')
    h.write('<div id = "navigation">\n')
    h.write('<ul class = "nav nav1">\n')
    h.write('''<li onclick = 'changelink("./intro.html")'>Introduction</li>\n''')
    h.write('''<li><p onclick = "expandhidechild(this)">Past papers</p> <ol class = "hidden nav nav2"><li \
        onclick = 'changelink("https://nickgmv.github.io/exampapers/exam_papers_maths.html")'>NCFE Past Papers </li>\n''')
    h.write('</li><li>MME Past Papers</li></ol>\n</li>')
    h.write('<li><p onclick = "expandhidechild(this)">Our 10 week course</p> <ol class = "hidden nav nav2">\n')
    

    for part in level1:
        os.mkdir(f'./{main_directory}/{part}')
        h.write( f'''<li onclick = 'changelink("./{part}/{part}.html")'>{part} sessions </li>\n''')
        report_success(f'{part} was found and added to the site build')
    


# checking this it is locating the entire directory for this repo



# generate actual lesson content now navigation pages are completed
for part in level1:
    part_name = f'{part}.html'
    #print(part)
    sections = os.listdir( f'{base_path}/{part}')
    report_success(f' sections in {part} are {sections} they will be added to site')


    with open(f'./{main_directory}/{part}/{part_name}', "w") as g:
        g.write('''<!DOCTYPE html>\n<html lang ="en">\n<link href="../fs_styles.css" type= "text/css" rel="stylesheet"/>\n<!--comment -->\n\n\n
        <link href="../fs_styles_content.css" type= "text/css" rel="stylesheet"/>''')
        g.write(f'<head>\n <title>{part} lessons </title>\n</head> \n<body>\n\n\n')
        #g.write('<div class = "buffer"></div>\n\n')
        g.write('<div class = "content_wrapper_sessions">')
        g.write(f'<h1>{part}</h1>')
        #g.write(f'<a href = "../main_page.html"> go back to main page </a>')
        for section in sections:
            g.write(f'<div class = "navbox"><a href = "./{part}_{section}_lessons.html"> {section} </a></div>')
        g.write('</div>')
        g.write('</body>')
        #g.write(nav_importer('../'))    
    #this loop will be refactored but for now it will iterate through the sections and build each lesson page
    for section in sections:
        page_name = f"./{main_directory}/{part}/{part}_{section}_lessons.html"

        #writing the opening html code for a lesson page
        with open(page_name,'w') as f:
            f.write(f'''<!DOCTYPE html>\n<html lang ="en">\n<link href="../fs_styles.css" type= "text/css" rel="stylesheet"/>\n
            <link href="../fs_styles_content.css" type= "text/css" rel="stylesheet"/><!--comment -->\n\n\n''')
            f.write(f'<head>\n <title>{part}{section} lessons </title>\n</head> \n<body>\n\n\n')
            #f.write('<div class = "buffer"></div>\n\n')
            f.write('<div class = content_wrapper_sessions>')
            f.write(f'<h1>{section}</h1>')
            f.write(f'<a href = "./{part}.html"> go back a level </a>')
            


            # now lesson page has been established find resource types.
            
            # find page plans and generate pages
            try:
                structure = os.listdir(f'{base_path}/{part}/{section}')
                report_success(f'found session structure for {part}{section}')
                #print(structure)
                structure = [file for file in structure if file.endswith('plan.xlsx') ]
                #print(structure)
                location = f'{base_path}/{part}/{section}/{structure[0]}'
                report_success(f'planning doc is located at {location}')
                lesson = pd.read_excel(f'{base_path}/{part}/{section}/{structure[0]}')
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
                pdf_path = f'{base_path}/{part}/{section}/exercises'
                # content\part_1\section_1\exercises\T01 Class Ex - Directed Numbers.pdf
                report_success(f'exercise pdfs were found in {pdf_path}')
                #pp = os.listdir(f'{base_path}/{section}')
                pp = os.listdir(f'{base_path}/{part}/{section}/exercises')
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

### old section for exam qs, this will now be a seperate page?
            #f.write(f'<h2> Get exam ready with exam practice </h2>')
#            try:
#                pdf_path = f'{base_path}/{part}/{section}/examqs'
#                # content\part_1\section_1\exercises\T01 Class Ex - Directed Numbers.pdf
#                report_success(f'exam pdfs were found in {pdf_path}')
#                #pp = os.listdir(f'{base_path}/{section}')
#                pp = os.listdir(f'{base_path}/{part}/{section}/examqs')
#                if pp:
#                    f.write(f'<h2> Get exam ready with exam practice </h2>')
#                    #print(pp)
#                    for pdf in pp:
#                        #print(pdf)
#                        f.write(f'<iframe class="pdf coached" src="../../content/{part}/{section}/examqs/{pdf}"  type="application/pdf" allow="fullscreen"></iframe>\n')
#                #for pdf in pdfs:
#                #f.write(f'<embed class="pdf coached" src="{pdf}" type="application/pdf">')
#            except:
#                report_issue(f'no exam folder present in {pdf_path}')
#            f.write('</div>')
            
#           #f.write(nav_importer('../'))
            #f.write()
            f.write('</body>')
h = open(main_page_path,'a')
h.write(f'''</ol><li onclick = 'changelink("./bios/bios.html")' >about us</li>''')
#endo fo nav list
# 
h.write('</ul>\n')
h.write('</div>\n')
#h.write('''<button id="fullscreen" >toggle full screen</button>''')
h.write('''<img id="fullscreen2" src = "./assets/screen button.png">''')

#add js script could compartmentalise this
h.write('''<script>
function changelink(link){
    var frame = document.getElementById('frame');
    frame.src = link;
}

//document.getElementById('fullscreen').addEventListener('click',()=>{
//    var frame = document.getElementById('frame')
 //   frame.classList.toggle('fullscreen')
//})

document.getElementById('fullscreen2').addEventListener('click',()=>{
    var frame = document.getElementById('frame')
    var button = document.getElementById('fullscreen2')
    frame.classList.toggle('fullscreen')
    button.classList.toggle('fullscreen')
})
function expandhidechild(doc){
    //window.alert(doc)
var child = doc.parentNode.childNodes;
//window.alert(child)
//child.classList.toggle("show");
//window.alert(child.classList);
child[2].classList.toggle("hidden");
}
</script>''')
h.write('</body>')
h.close
print(f'full process ran with {issue_count} reports in error report' )


