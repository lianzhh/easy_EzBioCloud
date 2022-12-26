import requests
import json
import time
import re

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from browsermobproxy import Server
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from Bio import SeqIO

import argparse

parser = argparse.ArgumentParser(description="Use selenium to upload 16S rRNA gene sequences automatically!")
parser.add_argument('-i', required=True, dest='fasta', help='16S rRNA gene files!')
parser.add_argument('-a', required=True, dest='account', help='EZBiocloud account, e.g. user@gmail.com')
parser.add_argument('-p', required=True, dest='passwd', help='EZBiocloud password')

args = parser.parse_args()
#write the install location of bowsermob-proxy
server = Server(r'D:\project\EZBio_16S_ID\browsermob-proxy-2.1.4\bin\browsermob-proxy.bat')

server.start()
proxy = server.create_proxy()


chrome_options = Options()
chrome_options.page_load_strategy = 'eager'
chrome_options.add_argument('--proxy-server={0}'.format(proxy.proxy))
chrome_options.add_argument('--ignore-certificate-errors')


s=Service('C:/Users/lianz/Downloads/chromedriver.exe')
driver = webdriver.Chrome(service=s)
base_url="https://www.ezbiocloud.net/identify"

account=args.account
passwd=args.passwd

wait = WebDriverWait(driver.get(base_url),10)

email = driver.find_element(By.XPATH,'//*[@id="emailVal"]').send_keys(account)
code= driver.find_element(By.XPATH,'//*[@id="passwordVal"]').send_keys(passwd)


driver.find_element(By.XPATH,'//*[@id="loginBtn"]').click()

#driver.find_elements_by_class_name("16S-based ID").click()
driver.refresh()
driver.refresh()

seq_count=0

for seq_record in SeqIO.parse(args.fasta, "fasta"):
    seqname=seq_record.id
    sequence=seq_record.seq
    driver.find_element(By.XPATH,'//span[@class="iconText"]').click()
    container1 = driver.find_element(By.ID,'modalSingleStrainUp')
    driver.execute_script("arguments[0].style.display = 'block';", container1)
    seqid = driver.find_element(By.XPATH,'//*[@id="sequenceName"]').send_keys(seqname)
    seqs = driver.find_element(By.XPATH,'//*[@id="ssurrnSeq"]').send_keys(sequence)
    driver.find_element(By.XPATH,'//*[@id="submitForReview"]').click()
    container2 = driver.find_element(By.ID,'modalMetaDataEdit')
    driver.execute_script("arguments[0].style.display = 'block';", container2)
    driver.find_element(By.XPATH,'//*[@id="completeSubmit"]').click()
    driver.refresh()
    time.sleep(3)
    seq_count += 1;
    
driver.refresh()
print('Upload finished!!!')
import pandas as pd
df1 = pd.DataFrame(columns=['Name','Top-hit taxon','Top-hit strain','Similarity','Top-hit taxonomy','Phylum'])

page = seq_count // 25
res = seq_count % 25
if(res ==0):
    for i in range(1, page + 1):
        for i in range(1, 26):
            print(i)
            name = driver.find_element(By.XPATH,'//*[@id="idResultTable"]/tbody/tr["i"]/td[3]').text
            hits = driver.find_element(By.XPATH,'//*[@id="idResultTable"]/tbody/tr["i"]/td[4]').text 
            strain = driver.find_element(By.XPATH,'//*[@id="idResultTable"]/tbody/tr["i"]/td[5]').text
            simi = float(driver.find_element(By.XPATH,'//*[@id="idResultTable"]/tbody/tr["i"]/td[6]').text)
            taxon = driver.find_element(By.XPATH,'//*[@id="idResultTable"]/tbody/tr["i"]/td[7]').text
            phylum = taxon.split(";")[1]
            df2 =  pd.DataFrame([[name,hits,strain,simi,taxon,phylum]],columns=['Name','Top-hit taxon','Top-hit strain','Similarity','Top-hit taxonomy','Phylum'])
            df1 = pd.concat([df1,df2])
        driver.find_element(By.LINK_TEXT, '›').click()
else:
    driver.find_element(By.LINK_TEXT, '›').click()
    for i in range(1, res + 1):
            name = driver.find_element(By.XPATH,'//*[@id="idResultTable"]/tbody/tr["i"]/td[3]').text
            hits = driver.find_element(By.XPATH,'//*[@id="idResultTable"]/tbody/tr["i"]/td[4]').text 
            strain = driver.find_element(By.XPATH,'//*[@id="idResultTable"]/tbody/tr["i"]/td[5]').text
            simi = float(driver.find_element(By.XPATH,'//*[@id="idResultTable"]/tbody/tr["i"]/td[6]').text)
            taxon = driver.find_element(By.XPATH,'//*[@id="idResultTable"]/tbody/tr["i"]/td[7]').text
            phylum = taxon.split(";")[1]
            df2 =  pd.DataFrame([[name,hits,strain,simi,taxon,phylum]],columns=['Name','Top-hit taxon','Top-hit strain','Similarity','Top-hit taxonomy','Phylum'])
            df1 = pd.concat([df1,df2])

df1.to_csv('user_data_ezbiocloud.csv') 

import matplotlib.pyplot as plt
g1= df1.groupby('Phylum')
plt.figure(figsize=(8, 6))
plt.pie(g1.size(),labels=g1.size().index)
plt.savefig('pie.png')
#plt.show()