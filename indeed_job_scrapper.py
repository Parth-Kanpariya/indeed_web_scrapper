#!/usr/bin/env python
# coding: utf-8

# In[2]:


from re import S
import requests
from bs4 import BeautifulSoup
import pandas as pd

joblist=[]

def extract(job,location,page):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}
    url = f"https://in.indeed.com/jobs?q={job}%20developer&l={location}&start={page}&vjk=0dd48d50b51e9bf7"
    r = requests.get(url, headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup

def transform(soup):
    divs = soup.find_all('div', class_='job_seen_beacon')
    for item in divs:
        title = item.find('a').text
        company = item.find('span',class_='companyName').text
        l=item.find('div',{'class':'job-snippet'}).findChildren()
        summary=" "
        for x in l:
            summary=summary+x.get_text()
        try:
            salary = item.find('div','attribute_snippet')
            salary=salary.get_text()   
        except:
            salary = ''  
        summary.replace('\n','')
        job={
            'title':title,
            'company':company,
            'salary':summary,
            'type':salary
        } 

        joblist.append(job)
        
        
        
    return



for i in range(0,40,10):
    c=extract("python","surat",i)
    transform(c)
    
df=pd.DataFrame(joblist)
print(df.head())
df.to_csv('jobs.csv')





# In[ ]:




