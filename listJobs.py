#! /usr/bin/python
''' This is a simple command line python program which fetches maximum 50 latest
    jobs from jobs.af API and accept two optional arguments (--category='job category
    --title='job title') and can filter jobs bassed on them, then it prints the result
    to a .xlsxworksheet with three sheets Male, Female and Any according the gender of
    jobs.
'''

import urllib2
import json
import sys
import csv
import xlsxwriter
import argparse

# Create an ArgumentParser
parser = argparse.ArgumentParser(description = 'Fetch and list maximum 50 latest\
                                jobs from "jobs.af" based on title, category, with \
                                both of them or with out of them.'
                                )
# Create arguments using argparse object
parser.add_argument('--category', help = "takes job category name or it's id ")
parser.add_argument('--title' , help = 'takes job title as string')

# Some variables used for flag.
job_title = ''
job_category = ''
flag = True

# Use tyr except to handle arguments parsing.
try:
    parser.parse_args([])
    args = parser.parse_args()

    # Assgin command line arguments to variables to pass them to urlBuilder method
    job_category = args.category
    job_title = args.title
except:
    flag = False
    print 'please enter your search like this patter: --category="catgory name" \
            --title="title name"'

# General url for jobs.af API
url = 'http://api.jobs.af/jobs?filter=1&per_page=50'

# Create the url(filter the request) to get data from jobs.af API
def url_builder(category = None, title = None):
    if category and title:
        title_query = title and '&position_title=' + title.replace(' ', '%20') or ''
        category_query = category and '&category=' + category.replace(' ', '%20') or ''
        global url
        return url + category_query + title_query
    
    elif category and not title:
        category_query = category and '&category=' + category.replace(' ', '%20') or ''
        return url + category_query
    
    elif title and not category:
        title_query = title and '&position_title=' + title.replace(' ', '%20') or ''
        return url + title_query
    
    else:
        url = 'http://api.jobs.af/jobs?per_page=50'
        return url


'''Get data from API as json object and get the specific parts of jobs and print them to
   a worksheet in differen sheet according to gender.
'''
def list_jobs(query):
    # Use urllib2 to load data as a json object.
    json_object = urllib2.urlopen(query)
    json_data = json.load(json_object)

    # Create a workboo using xlsxwriter to write data in it.
    workbook = xlsxwriter.Workbook('listJobs.xlsx')
    
    male_sheet = workbook.add_worksheet('Male')
    male_sheet.write_row('A1',['PSITION TITILE', 'SKILLS', 'EXPIRE-DATE',
                               'GENDER', 'LOCATION', 'CATEGORY'
                               ])
    
    female_sheet = workbook.add_worksheet('Female')
    female_sheet.write_row('A1',['PSITION TITILE', 'SKILLS', 'EXPIRE-DATE',
                                 'GENDER', 'LOCATION', 'CATEGORY'
                                 ])
    
    any_sheet = workbook.add_worksheet('Any')
    any_sheet.write_row('A1',['PSITION TITILE', 'SKILLS', 'EXPIRE-DATE',
                              'GENDER', 'LOCATION', 'CATEGORY'
                              ])
    
    # Open a CSV file.
    csv_file = open('jobs.csv', 'a')

    # Create an object of csv.writer to write to a csv file.
    csv_writer = csv.writer(csv_file)
    
    # Write to CSV file.
    csv_writer.writerow(['Position Title', 'skill', 'Expire Date', 'Gender',
                         'Location', 'Category'
                         ])

    # Counters
    any_counter = 1
    female_counter = 1
    male_counter = 1
    count = 0
    k = 0

    # Loop over dictionary to fetch jobs attributes 
    for item in json_data['data']:
        # Get items and encode and decode them to write items to xlsx files. 
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
        # Update counter for counting number of jobs that are ftching.
        count = count + 1
        
        # Get gender attribute and check it to specify the sheet to write in to it.
        gender = item['gender']
        
        if gender == 'Male':
            male_sheet.write_row(male_counter,k,[dtitle, dskills, dexpire,
                                                dgender, dstate, dcategory
                                                ])
            male_counter = male_counter + 1
            
        elif gender == 'Female':
            female_sheet.write_row(female_counter, k,[dtitle, dskills, dexpire,
                                                     dgender, dstate, dcategory
                                                     ])
            female_counter = female_counter + 1
            
        else:
            any_sheet.write_row(any_counter, k,[dtitle, dskills, dexpire, dgender,
                                               dstate, dcategory
                                               ])
            any_counter = any_counter + 1
            
        # Write to CSV file 
        csv_writer.writerow([title, skills, expire, gender, state, category])
        
    # Close workbook
    workbook.close()

    # Prompt for user based on the result of fetching of jobs from jobs.af
    result1 = ''
    result2 = ''
    if job_category == None:
        result1 = 'any category'
    else:
        result1 = job_category

    if job_title == None:
        result2 = 'any title.'
    else:
        result2 = job_title

        
    if count == 0:
        print 'No job/s were/was found in jobs.af for category: ' + str(result1) + \
              ' and title: ' + str(result2)
    elif job_category == None and job_title == None:
        print str(count) + '  latest jobs founded in jobs.af for category: ' + str(result1) + \
              ' and title: ' + str(result2) + ' were writen to listJobs.xlsx.'
        
        print str( any_counter -1 ) + ' of founded job/s are/is for any gender.'
        print str(male_counter -1) + ' of founded job/s are/is for males.'
        print str(female_counter -1) + ' of founded job/s are/is for females.'
    else:
        print str(count) + ' job/s were/was found in jobs.af for category: ' + str(result1) + \
              ' and title: ' + str(result2) + ' were writen to listJobs.xlsx.'
        
        print str( any_counter -1 ) + ' of founded job/s are/is for any gender.'
        print str(male_counter -1) + ' of founded job/s are/is for males.'
        print str(female_counter -1) + ' of founded job/s are/is for females.'


if flag == True:
    # Call urlBuilder method and assgin it's returned url to url variable
    url_query = url_builder(job_category, job_title)
    # Call listJobs method with the epecified URL
    list_jobs(url_query)
    
else:
    print 'Run program with correct argument pattern'


