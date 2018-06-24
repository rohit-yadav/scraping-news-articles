
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

