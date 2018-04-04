#! /usr/bin/python

'''This is a simple command line python program which fetch maximum 50 latest jobs from jobs.af API and accept two optional 
arguments (--category='job category --title='job title') and can filter jobs bassed on them and it print the result to a .xlsx
in three sheets Male, Female and Any according the gender of jobs.'''
import urllib2, json, sys, csv, xlsxwriter, argparse

#Create an ArgumentParser
parser = argparse.ArgumentParser(description = 'Fetch and list maximum 50 latest jobs from "jobs.af"\
                                                based on title, category, with both of them or with out of them.')
#create arguments using argparse object
parser.add_argument('--category', help = "takes job catgory name or it's id ")
parser.add_argument('--title' , help = 'takes job title as string')

#Some variables used for flag.
jobTitle = ''
jobCategory = ''
flag = True
try:
    parser.parse_args([])
    args = parser.parse_args()

    #assgin command line arguments to variables to pass them to urlBuilder method
    jobCategory = args.category
    jobTitle = args.title
except:
    flag = False
    print 'please enter your search like this patter: --category="catgory name" --title="title name"'

#Create the url( filter the request ) to get data from jobs.af API
def urlBuilder(category = None, title = None):
    if category and title:
        category = category.replace(' ', '_')
        title = title.replace(' ', '_')
        category = '&filter=1&category=' + category
        title = '&position_title=' + title
        url = 'http://api.jobs.af/jobs?per_page=50' + category + title
        print url
    elif category and not title:
        category = category.replace(' ','_')
        category = '&filter=1&category=' + category
        url = 'http://api.jobs.af/jobs?per_page=50' + category 
    elif title and not category:
        title = title.replace(' ', '_')
        title = '&filter=1&position_title=' + title
        url = 'http://api.jobs.af/jobs?per_page=50' + title
    else:
        url = 'http://api.jobs.af/jobs?per_page=50'
    return url

#Get data from API as json object and get the specific parts of jobs and print them to a worksheet in differen sheet according to gender.
def listJobs(query):
    #JSON object
    jsonObject = urllib2.urlopen(query)
    jsonData = json.load(jsonObject)

    #Xlsxwriter
    workbook = xlsxwriter.Workbook('listJobs.xlsx')
    Male_sheet = workbook.add_worksheet('Male')
    Male_sheet.write_row('A1',['PSITION TITILE', 'SKILLS', 'EXPIRE-DATE', 'GENDER', 'LOCATION', 'CATEGORY'])
    Female_sheet = workbook.add_worksheet('Female')
    Female_sheet.write_row('A1',['PSITION TITILE', 'SKILLS', 'EXPIRE-DATE', 'GENDER', 'LOCATION', 'CATEGORY'])
    Any_sheet = workbook.add_worksheet('Any')
    Any_sheet.write_row('A1',['PSITION TITILE', 'SKILLS', 'EXPIRE-DATE', 'GENDER', 'LOCATION', 'CATEGORY'])

    #CSV 
    csv_file = open('jobs.csv', 'a')
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Position Title', 'skill', 'Expire Date', 'Gender', 'Location', 'Category'])
    
    #Counters
    AnyCounter = 1
    FemaleCounter = 1
    MaleCounter = 1
    count = 0
    k = 0
    
    #Loop over dictionary to fetch jobs attributes 
    for item in jsonData['data']:
        #get items and encode and decode them to write items to xlsx files. 
        title = item['position_title'].encode('utf-8')
        dtitle = title.decode('unicode-escape')
        skills = item['skills_requirement'].encode('utf-8')
        dskills = skills.decode('unicode-escape')
        expire = item['expire_date'].encode('utf-8')
        dexpire = expire.decode('unicode-escape')
        gender = item['gender'].encode('utf-8')
        dgender = gender.decode('unicode-escape')
        
        loc = item.get('location').get('data')
        state = ''
        for i in range(len(loc)):
            province = loc[i] 
            state = state + province['name_en'].encode('utf-8')
            dstate = state.decode('unicode-escape')
            
        category = item.get('category').get('data')
        category = category['name_en'].decode('utf-8')
        dcategory = category.decode('unicode-escape')
        gender = item['gender']
        count = count + 1
        #specifiy the sheet to write jobs in it.
        if gender == 'Male':
            Male_sheet.write_row(MaleCounter,k,[dtitle, dskills, dexpire, dgender, dstate, dcategory])
            MaleCounter = MaleCounter + 1
            
        elif gender == 'Female':
            Female_sheet.write_row(FemaleCounter, k,[dtitle, dskills, dexpire, dgender, dstate, dcategory])
            FemaleCounter = FemaleCounter + 1
        else:
            Any_sheet.write_row(AnyCounter, k,[dtitle, dskills, dexpire, dgender, dstate, dcategory])
            AnyCounter = AnyCounter + 1
            
        # Write to CSV file 
        csv_writer.writerow([title, skills, expire, gender, state, category])
        
    workbook.close()

    #prompt for user based on the result of fetching of jobs from jobs.af
    result1 = ''
    result2 = ''
    if jobCategory == None:
        result1 = 'any category'
    else:
        result1 = jobCategory

    if jobTitle == None:
        result2 = 'any title.'
    else:
        result2 = jobTitle
    if count == 0:
        print 'No job/s were/was found in jobs.af for category: ' + str(result1) + ' and title: ' + str(result2)
    elif jobCategory == None and jobTitle == None:
        print str(count) + '  latest jobs founded in jobs.af for category: ' + str(result1) + ' and title: ' + str(result2) + ' were writen to listJobs.xlsx.'
        print str( AnyCounter -1 ) + ' of founded job/s are/is for any gender.'
        print str(MaleCounter -1) + ' of founded job/s are/is for males.'
        print str(FemaleCounter -1) + ' of founded job/s are/is for females.'
    else:
        print str(count) + ' job/s were/was found in jobs.af for category: ' + str(result1) + ' and title: ' + str(result2) + ' were writen to listJobs.xlsx.'
        print str( AnyCounter -1 ) + ' of founded job/s are/is for any gender.'
        print str(MaleCounter -1) + ' of founded job/s are/is for males.'
        print str(FemaleCounter -1) + ' of founded job/s are/is for females.'


if flag == True:
    
    #Call urlBuilder method and assgin it's returned url to url variable
    url = urlBuilder(jobCategory, jobTitle)

    #Call listJobs method with the epecified URL
    listJobs(url)
else:
    print 'Run program with correct argument pattern'


