# -*- coding: utf-8 -*-
"""
Created on Thu Sep 30 23:42:22 2021

@author: Saad
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import re
import pandas as pd
from selenium import webdriver
import logging

logging.basicConfig(level=logging.DEBUG)


chrome_options = Options()
chrome_options.add_argument("--headless")
opts = webdriver.ChromeOptions()
opts.headless =True
driver = webdriver.Chrome(executable_path = ChromeDriverManager().install(), options=opts)    
#driver = webdriver.Chrome(executable_path= r'C:\Users\Saad\.wdm\drivers\chromedriver\win32\94.0.4606.61\chromedriver.exe',
 #                        options=opts)

logging.debug('Chrome driver executed succesfully.')
def get_bestseller_links():
    """This is a convenient function will scrape amazon bestseller webpage links by departments"""
    
    driver.get('https://www.amazon.com/')
    bestsellerButton = driver.find_element_by_xpath('//*[@id="nav-xshop"]/a[1]')
    bestsellerButton.click()
    time.sleep(3)
    pageSource = driver.page_source
    soup_links = BeautifulSoup(pageSource, 'html.parser')
    links = soup_links.findAll('a', href=True)
    bestseller_links = re.findall('"/Best-Sellers-\s*(.*?)\s*"', str(links))
    bestseller_links_series = 'https://www.amazon.com/' + pd.Series(bestseller_links)

    if len(bestseller_links_series) > 0:
        logging.debug('Scraped bestseller links by departments from Amazon webpage.')
        return(bestseller_links_series)

    else:
        logging.debug('Trying the alternative xpath item.')
        driver.get('https://www.amazon.com/')
        bestsellerButton = driver.find_element_by_xpath('//*[@id="nav-xshop"]/a[2]')
        bestsellerButton.click()
        time.sleep(3)
        pageSource = driver.page_source
        soup_links = BeautifulSoup(pageSource, 'html.parser')
        links = soup_links.findAll('a', href=True)
        bestseller_links = re.findall('"/Best-Sellers-\s*(.*?)\s*"', str(links))
        bestseller_links_series = 'https://www.amazon.com/' + pd.Series(bestseller_links)
        #print(bestseller_links_series)
        logging.debug('Scraped Succesfully.')
        return(bestseller_links_series)


def parsing_to_df_function(item):
    """ This function will scrape top 50 items and takes Amazon Bestsellers webpage as an argument. 
    Recommended to use get_bestseller_links function to get bestseller links in a list to loop thorough"""
    try:
        driver.get(f'{item}')
        pageSource = driver.page_source
        soup = BeautifulSoup(pageSource, 'html.parser')
        logging.debug('Extract source code.')

        #Titles
        logging.debug('Parsing source code for titles.')
        titles = soup.findAll('div', {'class': 'a-section a-spacing-small'})
        pattern = "img alt=\'\\s*(.*?)\\s*\'|img alt=\"\\s*(.*?)\\s*\""
        titles_list = []
        for item in titles:
            function_titles = re.findall(f'{pattern}', str(item))
            titles_list.append(function_titles)
        title_series = pd.Series(titles_list)
        title_series = title_series.astype('str').str.replace('[\[\]\'\(\,\'\"\)]','').str.strip()

        # Reviews
        logging.debug('Parsing source code for reviews.')

        stars = soup.findAll('span', {'class': 'aok-inline-block zg-item'})
        star_list = []
        for item in stars:
            function_stars = re.findall('title="\s*(.*?)\s* stars"', str(item))
            star_list.append(function_stars)
        star_series = pd.Series(star_list, name='Star')   

        #Price
        logging.debug('Parsing source for prices.')

        price = soup.findAll('span', {'class': 'aok-inline-block zg-item'})
        price_list = []
        for item in price:
            function_price = re.findall('(\$\d+.\d+ ?-? ?\$\d+.\d+|\$\d+.\d+)', str(item.text))
            price_list.append(function_price)

        price_series = pd.Series(price_list)
        price_series = price_series.astype('str').str.replace('[\[\]\']','').str.strip()
  
        logging.debug('Combining series into DataFrame.')

        df = pd.DataFrame({'Title':title_series,'Stars':star_series,'Price':price_series})
        df.Stars = df.Stars.astype('str').str.replace('[\[\]\']','').str.strip().replace(r'^\s*$', 'Unknown', regex=True)
        return df

    except Exception as e: print(e)   
    print("""Error: The WebPage you are looking to parse does not have best seller items listed. Please make sure the webpage is valid""")