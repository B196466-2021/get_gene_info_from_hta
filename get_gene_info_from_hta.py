
import sys
import re
import os
import random
import time
import argparse
import pandas as pd
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

#starttime = time.time()
def get_gene_info_from(gene):
    url='https://www.proteinatlas.org/'+gene
    #class_name = "item-title.bold"
    #def wait(locator, timeout=10):
    #    """等到元素加载完成"""
    #    WebDriverWait(driver, timeout).until(EC.presence_of_element_located(locator))
    s = Service('C:\\Users\\11042\\AppData\\Local\\Microsoft\\WindowsApps\\msedgedriver.exe')
    WINDOW_SIZE = "2840,1460"
    edge_options = Options()
    edge_options.add_argument("--headless")
    edge_options.add_argument("--window-size=%s" % WINDOW_SIZE)
    edge_options.add_argument('--no-sandbox')
    edge_options.add_argument('--disable-gpu')
    driver = webdriver.Edge(service=s,options=edge_options)
    driver.get(url)
    #locator = (By.CLASS_NAME, class_name)
    #wait(locator)
    #driver.save_screenshot('C:\\Users\\spdx\\Desktop\\scripts\\rddc.tsinghua-gd\\all1.png')
    html  = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    #print(soup.prettify().encode('gb18030'))
    #print(soup.get_text())
    a=[x for x in soup.find_all("tbody")[7].get_text().strip('\n').split('\n') if x ]
    b={}
    for i in range(len(a)):
        if a[i] == 'Disease involvementi ':
            b[a[i]]=a[i+3]
        elif a[i].endswith('i '):
            b[a[i]]=a[i+2]
        else:
            continue
    e=pd.DataFrame(data=b,index=['Protein function']).T
    l=gene.split('-')
    with pd.ExcelWriter ('Breast_cancer_72_gene_from_HPA.xlsx',mode='a') as f:
        if len(l)==2:
            e.to_excel(f,sheet_name=l[1])
        else:
            e.to_excel(f,sheet_name=l[1]+'-'+l[2])
##匹配方式1
pat = '|'.join(r"\b{}\b".format(x) for x in aa.split('\n'))
gene['merge']=gene['Gene name'].str.findall(pat,flags=re.I).str.join(', ')
g=gene[(~pd.isnull(gene['merge'])) & (gene['merge']!='')]
g['merge1']=''
for x in g.iterrows():
    x[1]['merge1']=x[1]['Gene stable ID']+'-'+x[1]['Gene name']

result=g['merge1'].tolist()

with open('g.txt','w') as f:
    for x in result:
        f.write('{}\n'.format(x))

##通过检索HPA数据库，手动清理g.txt的重复项
for x in aa.split('\n'):
    get_gene_info_from(x)

##匹配方式2
l={}
for x in aa.split('\n'):
    l[x]='Yes'

gene['merge']=gene['Gene name'].map(b)
g=gene[gene['merge']=='Yes']

##
def get_gene_info_from(gene):
    url='https://www.proteinatlas.org/'+gene
    #class_name = "item-title.bold"
    #def wait(locator, timeout=10):
    #    """等到元素加载完成"""
    #    WebDriverWait(driver, timeout).until(EC.presence_of_element_located(locator))
    s = Service('C:\\Users\\spdx\\AppData\\Local\\Microsoft\\WindowsApps\\msedgedriver.exe')
    WINDOW_SIZE = "2840,1460"
    edge_options = Options()
    edge_options.add_argument("--headless")
    edge_options.add_argument("--window-size=%s" % WINDOW_SIZE)
    edge_options.add_argument('--no-sandbox')
    edge_options.add_argument('--disable-gpu')
    driver = webdriver.Edge(service=s,options=edge_options)
    driver.get(url)
    #locator = (By.CLASS_NAME, class_name)
    #wait(locator)
    #driver.save_screenshot('C:\\Users\\spdx\\Desktop\\scripts\\rddc.tsinghua-gd\\all1.png')
    html  = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    #print(soup.prettify().encode('gb18030'))
    #print(soup.get_text())
    a=[x for x in soup.find_all("tbody")[7].get_text().strip('\n').split('\n') if x ]
    b={}
    for i in range(len(a)):
        if a[i] == 'Disease involvementi ':
            b[a[i]]=a[i+3]
        elif a[i].endswith('i '):
            b[a[i]]=a[i+2]
        else:
            continue
    e=pd.DataFrame(data=b,index=['Protein function']).T
    return e

result=[]
for x in aa.split('\n'):
    result.append(get_gene_info_from(x))


pd.concat(result,keys=aa.split('\n'))

    