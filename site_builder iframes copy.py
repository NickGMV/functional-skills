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
    # put date tags in error and content reporting
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

    original3 = './backgroundfiles/message.html'
    target3 = f'{path}/message.html'
    shutil.copyfile(original3, target3)

def build_bios():
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
        <!--<div class = "content_wrapper"> -->
         ''')
        for index, row in bio_data.iterrows():
            b.write('<div class = "bio_section">\n')
            b.write(f'<h2>{row[0]}</h2>\n')
            b.write(f'<img class = "bio" src="../assets/bios/{row[1]}">\n')
            b.write(f'<p>{row[2]}</p>\n')
            b.write(f'<a href = "{row[3]}">{row[3]}</a>\n')
            b.write(f'<a href = "{row[4]}">Calendly</a>\n')
            b.write('</div>')
        #b.write('</div>')
        b.write('</body>\n')
        
     

# find the content folders from which to generate the site

# key files generated

# h - main page and navigation
# g - landing pages for sessions
# f - session content pages
# b - bios page 
# j - videos by topic

ind_path = './content/individual topics.xlsx'
pdfs_path = './content/individual topics pdfs'
base_path = './content/10week'
issue_count = 0
path = ""
main_directory = ""
parent_directory = ""


#create a universal parent directory for all generated content

#functions for basic set up

#set up folder structure and delete previous version
establish_build()
# copy assets and back ground files
copy_dependencies()
# open up error reporting session
initsession()
build_bios()

# creates the individual topic sections
topics_section_path = f"{parent_directory}/{main_directory}/individual_topics.html"
with open(topics_section_path,"w") as j:
    j.write('''<!DOCTYPE html>
<html lang ="en">
<link href="./fs_styles.css" type= "text/css" rel="stylesheet"/>
<!--comment -->


<head>
 <title>Maths functional skills - One stop shop </title>
 </head> 
<body>
 <div class ="buffer_small"></div>
 <div class = "content_wrapper">
 ''')
    topics = pd.read_excel(ind_path,0)
    ul = []
    
    for index,row in topics.iterrows():
        ul.append(f'<li><a href = "#{row[0]}">{row[0]}</a></li>\n')
        j.write('<div class = "topic">\n')
        j.write(f'<h2 id="{row[0]}"> {row[0]} </h2>\n')
        j.write(f'<iframe class = "vid" src = {row[1]} webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe>\n')
        j.write(f'<iframe class="pdf coached" src="../content/individual topics pdf/{row[2]}.pdf"  type="application/pdf" allow="fullscreen"></iframe>\n')
        j.write('<img class="fullscreen_topic" src = "./assets/screen button.png">')
        j.write('</div>\n')
    j.write('</div>\n </div>') 
    j.write('<div id = "navigation_individual">\n') 
    j.write('<input type="text" id="myInput" onkeyup="search()" placeholder="Search for content...">') 
    j.write('<ol id = "nav_list">\n') 
    for link in ul:
        j.write(link) 
    j.write('</ol>\n</div>\n')
    j.write('''
    <script>
function search() {
  // Declare variables
  var input, filter, ul, li, a, i, txtValue;
  input = document.getElementById('myInput');
  filter = input.value.toUpperCase();
  ul = document.getElementById("nav_list");
  li = ul.getElementsByTagName('li');

  // Loop through all list items, and hide those who don't match the search query
  for (i = 0; i < li.length; i++) {
    a = li[i].getElementsByTagName("a")[0];
    txtValue = a.textContent || a.innerText;
    if (txtValue.toUpperCase().indexOf(filter) > -1) {
      li[i].style.display = "";
    } else {
      li[i].style.display = "none";
    }
  }
}

var buttons = document.getElementsByClassName('fullscreen_topic')

for (let i =0;i<buttons.length;i++){
  buttons[i].addEventListener('click',(e)=>{
var topic = buttons[i].parentNode
window.alert(topic)
var button = this
window.alert(button)
topic.classList.toggle('fullscreen')
button.classList.toggle('fullscreen')
})
}
</script>''')
    j.write('</body>')


#find all the sub-parts (content sections/courses) load all parts and generate navigation pages
level1 = os.listdir(base_path)
report_success(f' content at the first level is {level1}\n\n\n')

main_page_path = f"{parent_directory}/{main_directory}/main_page.html"
with open(main_page_path ,"w") as h:
    
    # h refers to the main nav page being written by python in this loop
    h.write('<!DOCTYPE html>\n<html lang ="en">\n<link href="./fs_styles.css" type= "text/css" rel="stylesheet"/>\n<!--comment -->\n\n\n')
    h.write('<head>\n <title>Maths functional skills - One stop shop </title>\n </head> \n<body>\n\n\n')
    h.write('<div class = "buffer"></div>\n\n')
    h.write('<div class = "content_wrapper">\n')
    h.write('<iframe id = "frame" class = "viewer" src = "message.html" allow="fullscreen">\n')
    h.write('</iframe>\n')
    h.write('</div>\n')
    h.write('<div id = "navigation">\n')
    h.write('''<div id= "navigation_inner">\n''')
    h.write('<ul class = "nav nav1">\n')
    h.write('''<li onclick = 'changelink("./message.html")'>Introduction</li>\n''')
    h.write('''<li><p onclick = "expandhidechild(this)">Past papers</p> <ol class = "hidden nav nav2"><li \
        onclick = 'changelink("https://nickgmv.github.io/exampapers/exam_papers_maths.html")'>NCFE Past Papers </li>\n''')
    h.write('</li><li>MME Past Papers</li></ol>\n</li>')
    h.write('<li><p onclick = "expandhidechild(this)">Our 10 week course</p> <ol class = "hidden nav nav2">\n')
    

    # generate actual lesson content now navigation pages are completed
    for part in level1:
        part_name = f'{part}.html'
        #print(part)
        page_name = f"./{main_directory}/{part}/{part}.html"

        os.mkdir(f'./{main_directory}/{part}')
        
        h.write( f'''<li onclick = 'changelink("./{part}/{part}.html")'>{part}</li>\n''')
        
        report_success(f'{part} was found and added to the site build')


        #writing the opening html code for a lesson page
        with open(page_name,'w') as f:
            f.write(f'''<!DOCTYPE html>\n<html lang ="en">\n<link href="../fs_styles.css" type= "text/css" rel="stylesheet"/>\n
            <link href="../fs_styles_content.css" type= "text/css" rel="stylesheet"/><!--comment -->\n\n\n''')
            f.write(f'<head>\n <title>{part} lessons </title>\n</head> \n<body>\n\n\n')
            #f.write('<div class = "buffer"></div>\n\n')
            f.write('<div class = content_wrapper_sessions>')
            f.write(f'<h1>{part}</h1>')
            #f.write(f'<a href = "./{part}.html"> go back a level </a>')
            # now lesson page has been established find resource types.
            
            # find page plans and generate pages
            try:
                structure = os.listdir(f'{base_path}/{part}')
                report_success(f'found session structure for {part}')
                #print(structure)
                structure = [file for file in structure if file.endswith('plan.xlsx') ]
                #print(structure)
                location = f'{base_path}/{part}/{structure[0]}'
                report_success(f'planning doc is located at {location}')
                lesson = pd.read_excel(f'{base_path}/{part}/{structure[0]}')
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
                        # add code here to add to vids by topic section

                    elif row['Type']== 'quiz'  and str(row['Content']).lower() !='nan':
                        # function to build a quiz
                        quiz = 1
                    else:
                        report_issue(f'content type not recognised check your planning document for errors - find it at {location}')
            except:
                report_issue(f'There is an error with a planning doc check in {location} if there should be content for this section')
                #lesson = pd.read_excel(f'{base_path}/{part}/{section}/instructionsections/{structure[0]}')

                
            # find pdfs of exercises

            
            try:
                pdf_path = f'./{base_path}/{part}/notes'
                report_success(f'exercise notes were found in {pdf_path}')
                pp = os.listdir(f'{pdf_path}')
                if pp:
                    f.write(f'<h2> Accompanying notes for this session </h2>')
                    
                    for pdf in pp:
                        print(pdf)
                        f.write(f'<iframe class="pdf coached" src="../../content/10week/{part}/notes/{pdf}"  type="application/pdf" allow="fullscreen"></iframe>\n')
                
            except:
                report_issue(f'no pdf exercises folder present in {pdf_path} check if this is needed')

            f.write('</body>')







h = open(main_page_path,'a')
h.write('''</ol><li onclick = 'changelink("./individual_topics.html")'>Individual topics</li>\n''')
h.write(f'''<li onclick = 'changelink("https://calendly.com/functionalskillsbooking")' >Book a course or exam</li>''')
h.write(f'''<li onclick = 'changelink("./assets/spec.pdf")' >The functional maths specification</li>''')
h.write(f'''<li onclick = 'changelink("./bios/bios.html")' >About us</li>''')
#endo fo nav list
# 
h.write('</ul>\n')
h.write('</div>\n</div>\n')
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


