
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


# In[9]:


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


# **Orientation of the section pages**
# 
# In this newspaper there are basically two types of layouts: Grid View and List View. So we will filter the section of the grid and list view seperately. As depending upon the layouts the html fromat cahges, therefore we will have to scrap them differently.

# In[11]:


# Keep url of the section which has Grid layout
grid_layout_urls = [3, 4, 6, 7, 8, 9]

# All Grid half urls
grid_urls = []


# In[12]:


## Keep url of the section, which has linear layout(List) view
list_layout_urls = [0, 1, 5]

# All List half urls
list_urls = []


# In[13]:


# Extracting only Gride View section page urls
for filter_url in grid_layout_urls:
    grid_urls.append(section_urls[filter_url])


# In[14]:


# Extracting only List View section page urls
for filter_url in list_layout_urls:
    list_urls.append(section_urls[filter_url])


# In[15]:


# Checking the Grid View urls
grid_urls


# In[16]:


# Checking List view urls
list_urls

