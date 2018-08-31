
# coding: utf-8

# # Scraping News Aritcles - Hindi Newspaper

# ## Introduction
# 
# Scraping newspaper article from a newpaper website. A program that will navigate thorught the section of the newspaper and there pages to scrap news articles.

# In[1]:


# Import modules
import time
import urllib
import requests
import bs4
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# In[2]:


get_ipython().run_line_magic('matplotlib', 'inline')


# In[3]:


# Jagaran Newspaper's official url
url = "https://www.jagran.com"


# In[4]:


# Function to request a link
def request_url(link):
    """
    It takes a url and returns the html as string.
    """
    ## Slow things down ## 
    ## Let the site breath ##
    time.sleep(2)
    
    response = requests.get(link)
    html = response.text
    return html


# In[5]:


# Function to parse html
def parse_html(to_parse):
    """
    It takes a string, then parse it.
    Finally, it retuns a soup object.
    """
    soup = bs4.BeautifulSoup(to_parse, 'html.parser')
    return soup


# In[6]:


# Function to collect all sections links
# Like world news, national news ...

def all_section(main_url):
    """
    It takes a main url of the newspaper and then
    finds almost all the sections in the newspaper.
    Finally, it returns the section which we will scrap.
    """
    soup = parse_html(request_url(url))
    ul = soup.find("div", class_="MainLMenu tab").ul
    section_list = []
    for li in ul.find_all("li"):
        section_list.append(li.a.get('href'))
    # Remove the section which we will not consider
    # Like the video section and others
    remove = [0, 1, -1, -1, -1]
    for i in remove:
        section_list.remove(section_list[i])
    return section_list


# In[7]:


# All section url (half-urls)
section_urls = all_section(url)


# In[8]:


# Checking the sections urls
section_urls

