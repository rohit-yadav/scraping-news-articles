
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


# **Orientation of the section pages**
# 
# In this newspaper there are basically two types of layouts: Grid View and List View. So we will filter the section of the grid and list view seperately. As depending upon the layouts the html fromat cahges, therefore we will have to scrap them differently.

# In[9]:


# Keep url of the section which has Grid layout
grid_layout_urls = [3, 4, 6, 7, 8, 9]

# All Grid half urls
grid_urls = []


# In[10]:


## Keep url of the section, which has linear layout(List) view
list_layout_urls = [0, 1, 5]

# All List half urls
list_urls = []


# In[11]:


# Extracting only Gride View section page urls
for filter_url in grid_layout_urls:
    grid_urls.append(section_urls[filter_url])


# In[12]:


# Extracting only List View section page urls
for filter_url in list_layout_urls:
    list_urls.append(section_urls[filter_url])


# In[13]:


# Checking the Grid View urls
grid_urls


# In[14]:


# Checking List view urls
list_urls


# In[15]:


# Function to build complete url
# Returns a string
def complete_url(half_url):
    """
    This takes a second half of the url as input
    and then it adds the first part of the url.
    Finally it returns a complete url.
    """
   # Join the url with the href of world news
    full_url = url + half_url
    return full_url


# In[16]:


# To store comple urls of the Grid View
final_grid_urls =[]

# To store comple urls of the List View
final_list_urls =[]


# In[17]:


# Converting half urls to complete urls - Grid View
for url_get in grid_urls:
    final_grid_urls.append(complete_url(url_get))


# In[18]:


# Converting half urls to complete urls - List View
for url_set in list_urls:
    final_list_urls.append(complete_url(url_set))


# In[19]:


# Checking the full urls - Grid View
final_grid_urls


# In[20]:


# Checking the full urls - List View
final_list_urls


# In[21]:


# Check for valid urls
def valid_url(url):
    """
    Takes an url and checks if the urls is valid.
    Returns a boolearn value.
    """
    try:
        urllib2.urlopen(url)
        return True
    except Exception as e:
        return False


# In[22]:


# Collect article uls only for Grid view sections
def collect(page_urls):
    """
    Takes a list of urls which has a grid view layout,
    then it extracts the urls of the articles from it
    and then it returns it.
    """
    print("Extracting article urls from the following sections:")
    
    all_urls = set()
    for page_url in page_urls:
        print(page_url)
        soup_page = parse_html(request_url(page_url))
        for div in soup_page.find_all(class_="h3"):
            sec_head_href = div.find("a").get("href")
            # Checks if the url is valid
            # Add only if the url is valid
            if valid_url(sec_head_href):
                all_urls.add(sec_head_href)
            else:
                all_urls.add(complete_url(sec_head_href))
    return all_urls


# In[23]:


# Function call to collect all article urls from Grid View Sections
all_urls = collect(final_grid_urls)


# In[24]:


# Count the number of uniques aritcles urls
# Uncomment the below line to check the length
# len(all_urls)


# In[25]:


# Collects the article urls of the List view sections
def linear_layout_page(linear_url_list):
    """
    It takes urls of the list view sections and
    extracts the article links, then it returns it.
    """
    for url in linear_url_list:
        soup = parse_html(request_url(url))
        ul = soup.find("div", class_="newsFJagran").ul

        for li in ul.find_all("li"):
            # Adding to the existing urls from the Grid View sections
            all_urls.add(complete_url(li.a.get('href')))
        
    return all_urls


# In[26]:


# Funtion call to collect all the article urls - List View Sections
all_urls = linear_layout_page(final_list_urls)


# In[27]:


# Count - after adding articles urls from list view sections
# len(all_urls)


# In[28]:


# Takes list of urls
# Returns set with new set of urls
def navigator(navigate_url):
    """
    It takes urls of the List View sections and then navigates 
    to next page till the 10th page, along with it, it also add the page's url
    to list. Finally, it returns the list of urls of the pages.
    """
    next_page_url = []
    next_page_set = set()
    for navigate in navigate_url:
        soup = parse_html(request_url(navigate))
        url_class =  soup.find(class_="last")
        page_nav = url_class.a.get("href")
        page_nav = complete_url(page_nav)
        next_page_url = page_nav
        for _ in range(10):
            soup_next = parse_html(request_url(next_page_url))
            url_class_next =  soup_next.find(class_="last")
            page_nav_next = url_class_next.a.get("href")
            page_nav_next = complete_url(page_nav_next)
            next_page_url = page_nav_next
            next_page_set.add(next_page_url)
    return next_page_set


# In[29]:


# Function call to collect the links of different pages of the sections - List View sections only
aditional_url_set = navigator(final_list_urls)


# In[30]:


# Checking the length of the adtional urls from the pages of sections
# len(aditional_url_set)


# In[31]:


# Converting the set into list
aditional_url_list = list(aditional_url_set)


# In[32]:


# Extracting article lists from the additional urls list
all_urls = linear_layout_page(aditional_url_list)


# In[33]:


# Length of all urls
# len(all_urls)


# In[34]:


## To be used for text retivring texts of articles
article_urls_list = list(all_urls)


# In[35]:


df_final_urls = pd.DataFrame(article_urls_list)


# In[36]:


# Extracting all the urls to CSV file
df_final_urls.to_csv("final_urls.csv")


# In[37]:


# Function to extract article text

def article_text(article_urls):
    """
    It takes article urls list and scrap the 
    texts from it. Finally, it returns the text
    of the articles.
    """
    text = []
    for i in article_urls:
        article_soup = parse_html(request_url(i))
        div = article_soup.find("div", class_="articleBody")
        for child_div in div.find_all("div"):
            child_div.decompose()
        text.append(div.get_text())
    return text


# **Note:** *The below cell will take more than 16 minitus to execute.*
# 
# As we have to let the Jagran newspaper breath. We have given a delay of 2 seconds for extracting a article. So to extract 500 articles it will take atleast 1000 seconds.

# In[38]:


if len(article_urls_list) > 500:
    article_text_list = article_text(article_urls_list[0:500])
else:
    article_text_list = article_text(article_urls_list)


# In[39]:


text_df = pd.DataFrame(article_text_list)


# In[40]:


text_df.to_csv("articles_500.csv")


# ## Conclusion
# 
# Atlest 500 aritcle has been extracted from the Jagaran Newspaper with a crawler and exported into a csv file.
