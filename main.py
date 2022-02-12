# -*- coding: utf-8 -*-
"""
Created on Fri Feb  1 18:33:25 2019
东方财富个股研究网页的改版了，行业研究的没改。
@author: l
"""
from datetime import datetime
from selenium import webdriver
#from selenium.webdriver.common.action_chains import ActionChains #引入ActionChains鼠标操作类
#from selenium.webdriver.common.keys import Keys #引入keys类操作
import time
from selenium.webdriver.support.ui import WebDriverWait
import re
import requests
import pandas as pd
import os

file_industry_report_link = r'D:\code\python\report down url\ind report url 2019-11-08 22-53-41.txt'
file_stock_report_link = r'D:\code\python\report down url\stock report url 2019-11-08 23-02-08.txt'
site_stock_report = r'http://data.eastmoney.com/report/stock.jshtml'
site_industry_report = r'http://data.eastmoney.com/report/industry.jshtml'
site_broker_report = r'http://data.eastmoney.com/report/brokerreport.jshtml'


def filename_title_filter(text):
    text = text.replace(':', '')
    text = text.replace('/', '')
    text = text.replace("\\", '')
    text = text.replace('?', '')
    text = text.replace('"', '')
    text = text.replace('*', '')
    text = text.replace('|', '')
    text = text.replace('>', '')
    text = text.replace('<', '')
    return text

def filename_date_filter(text):
    return text.replace(':', '')


def scrape_stock(start_page = 1, scrape_page = 1, save_file=file_stock_report_link):#个股研报
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
#    browser = webdriver.Chrome(executable_path = r'D:\Download\chromedriver_win32\chromedriver.exe',  options=options)
    browser = webdriver.Chrome(executable_path = r'C:\Users\l\AppData\Local\Google\Chrome\Application\chromedriver.exe', options=options)#, chrome_options=options)# chrome_options=options)
    browser.get(site_stock_report)
    time.sleep(3)
    if scrape_page==None:
        total_page_text = WebDriverWait(browser, 5).until(lambda x: x.find_element_by_xpath('/html[1]/body[1]/div[6]/div[1]/div[1]/div[2]/div[2]/div[1]/a[7]')).text
        total_page = int(total_page_text)
    else:
        total_page = scrape_page

    with open(save_file, 'a+') as f:
        for page in range(start_page, total_page+1):
            WebDriverWait(browser, 5).until(lambda x: x.find_element_by_xpath("//input[@id='gotopageindex']")).clear()
            browser.find_element_by_xpath("//input[@id='gotopageindex']").send_keys(page)
            browser.find_element_by_xpath("//input[@value='Go']").click()
            time.sleep(3)
            
            page_sourece = browser.page_source
            
            res_link_list = re.findall('infocode=(.*?)"', page_sourece)
            res_link_list2 = [ "http://data.eastmoney.com/report/zw_stock.jshtml?infocode=%s\n"%i for i in res_link_list] 
        
#            res_link_list = re.findall('encodeUrl=(.*?)"', page_sourece)
#            res_link_list2 = [ "http://data.eastmoney.com/report/zw_stock.jshtml?encodeUrl=%s\n"%i for i in res_link_list] 
            '''
#            res_link_list = re.findall('"http://data.eastmoney.com/report/ReportRedirect.aspx(.*?)">', page_sourece)#报告的链接，返回一个50条的列表
#            res_link_list2 = ['http://data.eastmoney.com/report/ReportRedirect.aspx%s\n' %i.replace('&amp;','&') for i in res_link_list]
#            print(res_link_list2)
            '''
            f.writelines(res_link_list2)
            strTime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
            print( '个股 第%s页 采集数目%s  %s'%(page, len(res_link_list2), strTime))
            if len(res_link_list) == 50 and page!= total_page:
                time.sleep(0.01)
            else: 
                print( '提示： 第%s页 采集数目%s [数目不足] %s'%(page, len(res_link_list2), strTime))
    f.close()

def scrape_single(start_page = 1, scrape_page = None, save_file=file_industry_report_link, site=site_broker_report):#行业研报
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    browser = webdriver.Chrome(executable_path = r'C:\Users\l\AppData\Local\Google\Chrome\Application\chromedriver.exe', options=options)#, chrome_options=options)# chrome_options=options)
    browser.get(site)
    time.sleep(3)
    
    if scrape_page==None:
        total_page_text = WebDriverWait(browser, 5).until(lambda x: x.find_element_by_xpath('/html[1]/body[1]/div[5]/div[1]/div[1]/div[2]/div[2]/div[1]/a[7]')).text
        total_page = int(total_page_text)
    else:
        total_page = scrape_page

    with open(save_file, 'a+') as f:
        for page in range(start_page, total_page+1):
#            WebDriverWait(browser, 5).until(lambda x: x.find_element_by_xpath("//input[@id='gotopageindex']")).clear()
#            browser.find_element_by_xpath("//input[@id='gotopageind1ex']").send_keys(page)
#            browser.find_element_by_xpath("//input[@value='Go']").click()
#            WebDriverWait(browser, 5).until(lambda x: x.find_element_by_xpath('/html[1]/body[1]/div[5]/div[1]/div[1]/div[2]/div[2]/div[1]/input[1]')).clear()
#            browser.find_element_by_xpath('/html[1]/body[1]/div[5]/div[1]/div[1]/div[2]/div[2]/div[1]/input[1]').send_keys(page)
#            browser.find_element_by_xpath("//a[@class='btn_link']").click()
            time.sleep(3)
            
            page_sourece = browser.page_source
            res_link_list = re.findall('"encodeUrl":"(.*?)"', page_sourece)
            res_link_list2 = [ "http://data.eastmoney.com/report/zw_brokerreport.jshtml?encodeUrl=%s\n"%i for i in res_link_list] 
   
#            res_link_list = re.findall('/report/20(.*?)"', page_sourece)#报告的链接，返回一个50条的列表
#            res_link_list2 = ['http://data.eastmoney.com/report/20%s\n' %i for i in res_link_list]
            f.writelines(res_link_list2)
            strTime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
            print( '行业 第%s页 采集数目%s  %s'%(page, len(res_link_list2), strTime))
            if len(res_link_list) == 50 and page!= total_page:
                pass
            else:                
                print( '提示：第%s页 采集数目%s [数目不足] %s'%(page, len(res_link_list2), strTime))
    f.close()



def scrape_broker(start_page = 1, scrape_page = None, save_file=file_industry_report_link, site=site_broker_report):#行业研报
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    browser = webdriver.Chrome(executable_path = r'C:\Users\l\AppData\Local\Google\Chrome\Application\chromedriver.exe', options=options)#, chrome_options=options)# chrome_options=options)
    browser.get(site)
    time.sleep(3)
    
    if scrape_page==None:
        total_page_text = WebDriverWait(browser, 5).until(lambda x: x.find_element_by_xpath('/html[1]/body[1]/div[5]/div[1]/div[1]/div[2]/div[2]/div[1]/a[7]')).text
        total_page = int(total_page_text)
    else:
        total_page = scrape_page

    with open(save_file, 'a+') as f:
        for page in range(start_page, total_page+1):
            WebDriverWait(browser, 5).until(lambda x: x.find_element_by_xpath("//input[@id='gotopageindex']")).clear()
            browser.find_element_by_xpath("//input[@id='gotopageindex']").send_keys(page)
            browser.find_element_by_xpath("//input[@value='Go']").click()
#            WebDriverWait(browser, 5).until(lambda x: x.find_element_by_xpath('/html[1]/body[1]/div[5]/div[1]/div[1]/div[2]/div[2]/div[1]/input[1]')).clear()
#            browser.find_element_by_xpath('/html[1]/body[1]/div[5]/div[1]/div[1]/div[2]/div[2]/div[1]/input[1]').send_keys(page)
#            browser.find_element_by_xpath("//a[@class='btn_link']").click()
            time.sleep(3)
            
            page_sourece = browser.page_source
            res_link_list = re.findall('"encodeUrl":"(.*?)"', page_sourece)
            res_link_list2 = [ "http://data.eastmoney.com/report/zw_brokerreport.jshtml?encodeUrl=%s\n"%i for i in res_link_list] 
   
#            res_link_list = re.findall('/report/20(.*?)"', page_sourece)#报告的链接，返回一个50条的列表
#            res_link_list2 = ['http://data.eastmoney.com/report/20%s\n' %i for i in res_link_list]
            f.writelines(res_link_list2)
            strTime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
            print( '按机构下载 第%s页 采集数目%s  %s'%(page, len(res_link_list2), strTime))
            if len(res_link_list) == 50 and page!= total_page:
                pass
            else:                
                print( '提示：第%s页 采集数目%s [数目不足] %s'%(page, len(res_link_list2), strTime))
    f.close()

def scrape_industry_OLD(start_page = 1, scrape_page = None, save_file=file_industry_report_link):#行业研报
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    browser = webdriver.Chrome(executable_path = r'C:\Users\l\AppData\Local\Google\Chrome\Application\chromedriver.exe', options=options)#, chrome_options=options)# chrome_options=options)
    browser.get(site_industry_report)
    time.sleep(3)
    
    if scrape_page==None:
        total_page_text = WebDriverWait(browser, 5).until(lambda x: x.find_element_by_xpath('/html[1]/body[1]/div[5]/div[1]/div[1]/div[2]/div[2]/div[1]/a[7]')).text
        total_page = int(total_page_text)
    else:
        total_page = scrape_page

    with open(save_file, 'a+') as f:
        for page in range(start_page, total_page+1):
            WebDriverWait(browser, 5).until(lambda x: x.find_element_by_xpath("//input[@id='gotopageindex']")).clear()
#            WebDriverWait(browser, 5).until(lambda x: x.find_element_by_xpath("//input[@id='gotopageindex']")).clear()
            browser.find_element_by_xpath("//input[@id='gotopageindex']").send_keys(page)
            browser.find_element_by_xpath("//input[@value='Go']").click()
#            WebDriverWait(browser, 5).until(lambda x: x.find_element_by_xpath('/html[1]/body[1]/div[5]/div[1]/div[1]/div[2]/div[2]/div[1]/input[1]')).clear()
#            browser.find_element_by_xpath('/html[1]/body[1]/div[5]/div[1]/div[1]/div[2]/div[2]/div[1]/input[1]').send_keys(page)
#            browser.find_element_by_xpath("//a[@class='btn_link']").click()
            time.sleep(3)
            
            page_sourece = browser.page_source
            res_link_list = re.findall('"encodeUrl":"(.*?)"', page_sourece)
            res_link_list2 = [ "http://data.eastmoney.com/report/zw_industry.jshtml?encodeUrl=%s\n"%i for i in res_link_list] 
   
#            res_link_list = re.findall('/report/20(.*?)"', page_sourece)#报告的链接，返回一个50条的列表
#            res_link_list2 = ['http://data.eastmoney.com/report/20%s\n' %i for i in res_link_list]
            f.writelines(res_link_list2)
            strTime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
            print( '行业 第%s页 采集数目%s  %s'%(page, len(res_link_list2), strTime))
            if len(res_link_list) == 50 and page!= total_page:
                pass
            else:
                
                print( '提示：第%s页 采集数目%s [数目不足] %s'%(page, len(res_link_list2), strTime))
    f.close()


def scrape_industry(start_page = 1, scrape_page = 2, save_file=file_industry_report_link):#行业研报
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    browser = webdriver.Chrome(executable_path = r'C:\Users\l\AppData\Local\Google\Chrome\Application\chromedriver.exe', options=options)#, chrome_options=options)# chrome_options=options)
    browser.get(site_industry_report)#打开网页
    time.sleep(3)

#    options = webdriver.ChromeOptions()
    options.add_argument('headless')
#    browser = webdriver.Chrome(executable_path = r'D:\Download\chromedriver_win32\chromedriver.exe',  options=options)
#    browser = webdriver.Chrome(executable_path = r'C:\Users\l\AppData\Local\Google\Chrome\Application\chromedriver.exe', options=options)#, chrome_options=options)# chrome_options=options)
#    browser.get(site_stock_report)
#    time.sleep(3)
# 
    if scrape_page==None:
        total_page_text = WebDriverWait(browser, 5).until(lambda x: x.find_element_by_xpath('/html[1]/body[1]/div[5]/div[1]/div[1]/div[2]/div[2]/div[1]/a[7]')).text
        total_page = int(total_page_text)
    else:
        total_page = scrape_page

    out = []
    with open(save_file, 'a+') as f:
        for page in range(start_page, total_page+1):
#            browser.get(site_industry_report)#打开网页
#            time.sleep(3)

            WebDriverWait(browser, 5).until(lambda x: x.find_element_by_xpath("//input[@id='gotopageindex']")).clear()
            browser.find_element_by_xpath("//input[@id='gotopageindex']").send_keys(page)
            browser.find_element_by_xpath("//input[@value='Go']").click()
            time.sleep(3)
            
            page_sourece = browser.page_source
            out.append(page_sourece)
            
            res_link_list = re.findall('infocode=(.*?)"', page_sourece)
            res_link_list2 = [ "http://data.eastmoney.com/report/zw_industry.jshtml?infocode=%s\n"%i for i in res_link_list] 
#            res_link_list = re.findall('encodeUrl=(.*?)"', page_sourece)
#            res_link_list2 = [ "http://data.eastmoney.com/report/zw_industry.jshtml?encodeUrl=%s\n"%i for i in res_link_list] 
#            print(res_link_list2[0])
            f.writelines(res_link_list2)
            strTime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
            print( '行业 第%s页 采集数目%s  %s'%(page, len(res_link_list2), strTime))
            if len(res_link_list) == 50 and page!= total_page:
                pass
            else:                
                print( '提示：第%s页 采集数目%s [数目不足] %s'%(page, len(res_link_list2), strTime))
    f.close()
    return out

def down_industry(start_line = 1, save_file=file_industry_report_link, sleep_sec=2):    
    report_lis = pd.Series(list(open(save_file))).dropna()
#    downloaded_str = downloaded.read()
    browsered = r'D:\code\python\industry browsered.txt'
    downloaded =  r'D:\code\python\download2.txt'
#    browsered_str = open( browsered, 'r').read()
#    downloaded_str = open(downloaded, 'r').read()
    file_exist_counter = 0
    
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    browser2 = webdriver.Chrome(executable_path = r'C:\Users\l\AppData\Local\Google\Chrome\Application\chromedriver.exe', options=options)

    for i in range(start_line, len(report_lis)):
        try:
            strTime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
            link = report_lis[i].replace('\n','')  
#            browsered_str = open( browsered, 'r').read()
            print('%s [行业] 开始于%s'%(i, start_line))
            if 1==2:
#            if (link in browsered_str) :
                print(i, '[已浏览] %s'%strTime)
            else:
                browser2.get(link)
                time.sleep(sleep_sec)
                page_sourece = browser2.page_source
#                report_title = re.findall('"title":"(.*?)"', page_sourece)[0]                
#                report_date = re.findall('"publishDate":"(.*?)"', page_sourece)[0]
#                report_broker = re.findall('"orgSName":"(.*?)"', page_sourece)[0]
#                report_author = re.findall('"researcher":"(.*?)"', page_sourece)[0]              
                
                
                report_date = re.findall('notice_date":"(.*?)"', page_sourece)[0]
                report_title = re.findall('"notice_title":"(.*?)"', page_sourece)[0]
#                stock_name = re.findall('"short_name":"(.*?)"', page_sourece)[0]
                report_author = re.findall('"researcher":"(.*?)"', page_sourece)[0]
                report_broker = re.findall('"source_sample_name":"(.*?)"', page_sourece)[0]                
#                /html[1]/body[1]/div[4]/div[2]/div[3]/div[1]/div[1]/h1[1]
#                report_title = browser2.find_element_by_xpath('/html[1]/body[1]/div[3]/div[1]/div[3]/div[1]/div[1]/div[1]/h1[1]').text
#                report_date = browser2.find_element_by_xpath('/html[1]/body[1]/div[3]/div[1]/div[3]/div[1]/div[1]/div[2]/span[2]').text
#                report_broker = browser2.find_element_by_xpath('/html[1]/body[1]/div[3]/div[1]/div[3]/div[1]/div[1]/div[2]/span[3]').text
#                report_author = browser2.find_element_by_xpath('/html[1]/body[1]/div[3]/div[1]/div[3]/div[1]/div[1]/div[2]/span[4]').text
                report_date = filename_date_filter(report_date)
                report_title = filename_title_filter(report_title)  
                filename = "D:\code\python\industry report\%s %s %s %s.pdf"%(report_date, report_title, report_broker, report_author)
                
                with open(browsered, 'a+') as f3:
                    f3.write(link)
                if os.path.exists(filename):
                    print(i ,'[文件存在]  %s'%(strTime))
                    file_exist_counter +=1
    
                else:
#                    page_sourece = browser2.page_source
#                    match_pdf = re.findall("attachUrl":"(.*?)", page_sourece)[0]
#                    match_pdf = re.findall('pdf.(.*?)"', page_sourece)
                    match_pdf =re.findall('"attach_url":"(.*?)"', page_sourece)
#                    match_pdf  = re.findall('http://(.*?).pdf"|http://(.*?).PDF"', page_sourece)
#                    match_pdf2 = re.findall('http://(.*?).PDF"', page_sourece)
                    
#                    print(match_pdf)
                    if len(match_pdf) ==0:
                        print(i, '[无下载地址] %s'%strTime)
                    else:
#                        if match_pdf[0][0]!='':
#                            pdf_url = 'http://%s.pdf' %(match_pdf[0][0])
#                        else:
#                            pdf_url = 'http://%s.PDF' %(match_pdf[0][1])
#                        pdf_url = "http://pdf.%s"% match_pdf[0]
#                        print("下载地址", pdf_url)                        
                        r = requests.get(match_pdf[0]) 
                        with open(filename, 'wb') as f:
                            f.write(r.content)                            
                        print(i , '[完成下载]  %s'%(strTime))
                        time.sleep(0.01)
        except Exception as e:
            print(e)
    browser2.quit()

def down_broker(start_line = 0, save_file=file_industry_report_link, sleep_sec=2):    
    report_lis = pd.Series(list(open(save_file))).dropna()
#    downloaded_str = downloaded.read()
    browsered = r'D:\code\python\industry browsered.txt'
    downloaded =  r'D:\code\python\download2.txt'
#    browsered_str = open( browsered, 'r').read()
#    downloaded_str = open(downloaded, 'r').read()
    file_exist_counter = 0
    
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    browser2 = webdriver.Chrome(executable_path = r'C:\Users\l\AppData\Local\Google\Chrome\Application\chromedriver.exe', options=options)

    for i in range(start_line, len(report_lis)):
        try:
            strTime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
            link = report_lis[i].replace('\n','')  
#            browsered_str = open( browsered, 'r').read()
            print('%s [券商] 开始于%s'%(i, start_line))
            if 1==2:
#            if (link in browsered_str) :
                print(i, '[已浏览] %s'%strTime)
            else:
                browser2.get(link)
                time.sleep(sleep_sec)
                page_sourece = browser2.page_source
                report_title = re.findall('"title":"(.*?)"', page_sourece)[0]                
                report_date = re.findall('"publishDate":"(.*?)"', page_sourece)[0]
                report_broker = re.findall('"orgSName":"(.*?)"', page_sourece)[0]
                
                report_author = re.findall('"researcher":"(.*?)"', page_sourece)[0]              
#                print(report_author)
#                /html[1]/body[1]/div[4]/div[2]/div[3]/div[1]/div[1]/h1[1]
#                report_title = browser2.find_element_by_xpath('/html[1]/body[1]/div[3]/div[1]/div[3]/div[1]/div[1]/div[1]/h1[1]').text
#                report_date = browser2.find_element_by_xpath('/html[1]/body[1]/div[3]/div[1]/div[3]/div[1]/div[1]/div[2]/span[2]').text
#                report_broker = browser2.find_element_by_xpath('/html[1]/body[1]/div[3]/div[1]/div[3]/div[1]/div[1]/div[2]/span[3]').text
#                report_author = browser2.find_element_by_xpath('/html[1]/body[1]/div[3]/div[1]/div[3]/div[1]/div[1]/div[2]/span[4]').text
                report_date = filename_date_filter(report_date)
                report_title = filename_title_filter(report_title)
                filename = "D:\code\python\industry report\%s %s %s %s.pdf"%(report_date, 
                            report_title, report_broker, report_author)
#                filename = "D:\code\python\industry report\%s %s %s %s %s.pdf"%(report_date, 
#                            report_title, report_broker, report_author, strTime.replace(":",""))          
                with open(browsered, 'a+') as f3:
                    f3.write(link)
                if os.path.exists(filename):
                    print(i ,'[文件存在]  %s'%(strTime))
                    file_exist_counter +=1
    
                else:
#                    page_sourece = browser2.page_source
#                    match_pdf = re.findall("attachUrl":"(.*?)", page_sourece)[0]
#                    match_pdf = re.findall('pdf.(.*?)"', page_sourece)
                    match_pdf  = re.findall('http://(.*?).pdf"|http://(.*?).PDF"', page_sourece)
#                    match_pdf2 = re.findall('http://(.*?).PDF"', page_sourece)
                    
#                    print(match_pdf)
                    if len(match_pdf) ==0:
                        print(i, '[无下载地址] %s'%strTime)
                    else:
                        if match_pdf[0][0]!='':
                            pdf_url = 'http://%s.pdf' %(match_pdf[0][0])
                        else:
                            pdf_url = 'http://%s.PDF' %(match_pdf[0][1])
#                        pdf_url = "http://pdf.%s"% match_pdf[0]
#                        print("下载地址", pdf_url)                        
                        r = requests.get(pdf_url) 
                        with open(filename, 'wb') as f:
                            f.write(r.content)                            
                        print(i , '[完成下载]  %s'%(strTime))
                        time.sleep(0.01)
        except Exception as e:
            print(e)
    browser2.quit()




def down_stock(start_line = 1, save_file=file_stock_report_link, sleep_sec=2):
    report_lis = pd.Series(list(open(save_file))).dropna()
#    report_lis = pd.Series(list(open(r'D:\code\python\report url5.txt'))).dropna()
#    downloaded_str = downloaded.read()
    browsered = r'D:\code\python\stock browsered2.txt'
#    download = r'D:\code\python\stock download.txt'
#    browsered_str = open( browsered, 'r').read()
#    downloaded_str = open(downloaded.read(), 'r').read()
    file_exist_counter = 0
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    browser2 = webdriver.Chrome(executable_path = r'C:\Users\l\AppData\Local\Google\Chrome\Application\chromedriver.exe', options=options)

    for i in range(start_line, len(report_lis)):
        try:
            strTime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
            link = report_lis[i].replace('\n','')  
    #            browsered_str = open( browsered, 'r').read()
            print('%s [股票] 开始于%s'%(i, start_line))
    
            if 1==2:
    #            if (link in browsered_str):
                print(i, '[已浏览] %s'%strTime)
            else:
                browser2.get(link)
                time.sleep(sleep_sec)
           
                page_sourece = browser2.page_source
#                print(page_sourece)
#                with open(r'D:\123.txt','w', encoding='utf-8') as ff:
#                    ff.write(page_sourece)
                
#                stock_name = re.findall('"stockName":"(.*?)"', page_sourece)[0]
#                report_title = re.findall('"title":"(.*?)"', page_sourece)[0]                
#                report_date = re.findall('"publishDate":"(.*?)"', page_sourece)[0]
#                report_broker = re.findall('"orgSName":"(.*?)"', page_sourece)[0]
#                report_author = re.findall('"researcher":"(.*?)"', page_sourece)[0]  
#                
                
                report_date = re.findall('notice_date":"(.*?)"', page_sourece)[0]
                report_title = re.findall('"notice_title":"(.*?)"', page_sourece)[0]
                stock_name = re.findall('"short_name":"(.*?)"', page_sourece)[0]
                report_author = re.findall('"researcher":"(.*?)"', page_sourece)[0]
                report_broker = re.findall('"source_sample_name":"(.*?)"', page_sourece)[0]
                
#                stock_name = browser2.find_element_by_xpath('/html[1]/body[1]/div[4]/div[2]/div[1]/div[1]/div[1]/a[1]').text
#                report_title = browser2.find_element_by_xpath(' /html[1]/body[1]/div[4]/div[2]/div[3]/div[1]/div[1]/h1[1]').text
#                report_date = browser2.find_element_by_xpath('/html[1]/body[1]/div[4]/div[2]/div[3]/div[1]/div[1]/div[1]/span[2]').text
#                report_broker = browser2.find_element_by_xpath('/html[1]/body[1]/div[4]/div[2]/div[3]/div[1]/div[1]/div[1]/span[3]').text
#                report_author = browser2.find_element_by_xpath('/html[1]/body[1]/div[4]/div[2]/div[3]/div[1]/div[1]/div[1]/span[4]').text
                report_date = filename_date_filter(report_date)
                report_title = filename_title_filter(report_title)
                stock_name = filename_title_filter(stock_name)                   
                filename = "D:\code\python\stock report\%s %s %s %s %s.pdf"%( report_date, stock_name, report_title, report_broker, report_author)
#                print(filename)
            
                with open(browsered, 'a+') as f3:
                    f3.write(link)
                    
                if os.path.exists(filename):
                    print(i ,'[文件存在]  %s'%(strTime))
                    file_exist_counter +=1
    
                else:
                    match_pdf =re.findall('"attach_url":"(.*?)"', page_sourece)
#                    match_pdf = re.findall('pdf.(.*?)"', page_sourece)
                    
                    if len(match_pdf) ==0:
                        print(i, '[无下载地址] %s'%strTime)
                    else:
                        
#                        pdf_url =  match_pdf[0]                        
                        r = requests.get( match_pdf[0] ) 
#                        print(filename)
                        with open(filename, 'wb') as f:
                            f.write(r.content)                            
                        print(i , '[完成下载]  %s'%(strTime))
                        time.sleep(0.01)
        except Exception as e:
            print(e)
    browser2.quit()


def daily_task_stock( scrape_page=4, start_line=0):
    datetime_str = datetime.now().strftime(datetime.now().strftime("%Y-%m-%d %H-%M-%S"))
    fn_stock = r'D:\code\python\report down url\stock report url %s.txt'%datetime_str
    print(fn_stock)
    scrape_stock(scrape_page = scrape_page, save_file = fn_stock)
    down_stock(save_file = fn_stock, start_line = start_line)

def daily_task_ind( scrape_page=4, start_line=0):
    datetime_str = datetime.now().strftime(datetime.now().strftime("%Y-%m-%d %H-%M-%S"))
    fn_industry = r'D:\code\python\report down url\ind report url %s.txt'%datetime_str
    print(fn_industry)
    scrape_industry(scrape_page = scrape_page, save_file = fn_industry)
    down_industry(save_file = fn_industry, start_line = start_line)

def daily_task_bro( scrape_page=4, start_line=0):
    datetime_str = datetime.now().strftime(datetime.now().strftime("%Y-%m-%d %H-%M-%S"))
    fn_bro = r'D:\code\python\report down url\broker report url %s.txt'%datetime_str
    print(fn_bro)
    scrape_broker(scrape_page = scrape_page, save_file = fn_bro)
    down_broker(save_file = fn_bro, start_line = start_line)

def get_filename(path=r'D:\code\python\industry report'):
    out = []
    for root, dirs,files in os.walk(path):
        for name in files:
            if 'report' in name:
                out.append(os.path.join(root, name))
    return out

def rename_run(path=r'D:\code\python\industry report'):
    lis = get_filename(path)
    for i in lis:
        try:
            new_filename = i.replace('Dcodepythonindustry report', '')
            os.rename(i, new_filename)
        except Exception as e:
            print(e)

def down_single_page(scrape_page=4, start_line=0,
                       site='http://data.eastmoney.com/report/orgpublish.jshtml?orgcode=80086668'):
    datetime_str = datetime.now().strftime(datetime.now().strftime("%Y-%m-%d %H-%M-%S"))
    fn_bro = r'D:\code\python\report down url\broker report url %s.txt'%datetime_str
    print(fn_bro)
    scrape_single(scrape_page = scrape_page, save_file = fn_bro, site=site)
    down_broker(save_file = fn_bro, start_line = start_line)    
    return



if __name__ == '__main__':

    daily_task_stock(50)
    daily_task_ind(50)
    daily_task_bro(50)
