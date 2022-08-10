from re import S
import requests
from bs4 import BeautifulSoup
import pandas as pd
import smtplib
from email.mime.text import MIMEText as text


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



#extracting 
for i in range(0,40,10):
    c=extract("python","surat",i)
    transform(c)
    
    
    

message="Job openings:- \n"


for i in joblist:
    if i['title'] == "Python Developer":
        message+="\n"+i['title']+" at "+i['company']
      
    
msg = text(message)
msg['Subject'] = 'Indeed Job Opening For Python Developer'
msg['From'] = "parthkanpariya4@gmail.com"
msg['To'] = "parthkanpariya4@gmail.com"    


    
    
 #email content   
smtp_object = smtplib.SMTP("smtp.gmail.com", 587)

smtp_object.ehlo()
smtp_object.starttls()
smtp_object.login("parthkanpariya4@gmail.com","bcgrwoyyaexvxspf")

smtp_object.sendmail("parthkanpariya4@gmail.com","parthkanpariya4@gmail.com",msg.as_string())
smtp_object.quit()
   
#convert to csv from panda
df=pd.DataFrame(joblist)
print(df.head())
df.to_csv('jobs.csv')




