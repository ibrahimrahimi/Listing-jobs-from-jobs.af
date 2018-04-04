# List-Jobs
This is a simple command line python program which fetches maximum 50 latest jobs from jobs.af API and it can fiters jobs by jobs categry and jobs titile or both of them, then it writes the result to a .xlsx file in three different sheets based on jobs gender and also write result to a CSV file too.
You can run this program in command line and it has two optional arguments for filtering jobs you want to fetch. for passing arguments to this program you should pass job category or job tilte or both of them following this pattern. 
for filtering jobs based on category and title: ./listJogs.py --catgory='job category' --tilte='job title' 
for filtering jobs based on category: ./listJogs.py --catgory='job category' 
for filtering jobs based on title: ./listJogs.py  --tilte='job title'
with out any filtering: ./listJogs.py
