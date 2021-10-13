# SCRAPE MARS PYTHON FILE

# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import requests
import pandas as pd

def scrape():

    # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    ####################
    ## NASA Mars News ##
    ####################

    # URL of page to be scraped
    url = 'https://redplanetscience.com/'

    # Visit url
    browser.visit(url)

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(browser.html, 'html.parser')

    print(soup.select_one('div.list_text'))

    news_title = soup.find_all('div', class_='col-md-8')[0].find('div',class_='content_title').text

    news_p = soup.find_all('div', class_='col-md-8')[0].find('div',class_='article_teaser_body').text

    ###########################
    ## JPL Mars Space Images ##
    ###########################

    # URL of page to be scraped
    images_url = 'https://spaceimages-mars.com/'

    # Visit url
    browser.visit(images_url)

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(browser.html, 'html.parser')


    img_url_ext = soup.find_all('a', class_='showimg fancybox-thumbs')[0].attrs['href']
    featured_image_url = images_url + img_url_ext

    ################
    ## Mars Facts ##
    ################

    # URL of page to be scraped
    facts_url = 'https://galaxyfacts-mars.com/'

    tables = pd.read_html(facts_url)

    mars_facts_df = tables[1]
    mars_facts_df.columns = ["Fact Descriptor", "Value"]


    mars_facts_html_table = mars_facts_df.to_html()

    ######################
    ## Mars Hemispheres ##
    ######################

    # URL of page to be scraped
    hemi_url = 'https://marshemispheres.com/'

    # Visit url
    browser.visit(hemi_url)

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(browser.html, 'html.parser')

    mars_hemispheres = soup.find_all('div', class_='item')

    # Create list for each hemisphere title and image url
    title_list = []
    url_list = []

    for i in mars_hemispheres:
        # Collect titles and append to list
        title_list.append(i.find('div', class_='description').find('h3').text)
        
        # Collect image link by browsing to hemisphere page
        img_page_link = i.find('a', class_='itemLink product-item')['href']

        # String together main url + image page link and click on link
        browser.visit(f'{hemi_url}{img_page_link}')
        
        # Create BeautifulSoup object; parse with 'html.parser'
        img_page_soup = BeautifulSoup(browser.html, 'html.parser')
        
        # Locate image url for full-resolution photo
        img_url = img_page_soup.find('div', class_='downloads').find_all('li')[0].find('a')['href']
        
        # Append image urls to a list 
        url_list.append(f'{hemi_url}{img_url}')
        
        # Go back to home page
        browser.back
        
    browser.quit()

    # Create a list of dictionaries 
    hemisphere_image_urls = []

    for i, j in zip(title_list, url_list):
        hemisphere_image_urls.append({"title": i, "img_url": j})

    mars_dict = {
        "news_title":news_title,
        "news_p":news_p,
        "featured_img_url":featured_image_url,
        "facts_table":mars_facts_html_table,
        "hemisphere_imgs":hemisphere_image_urls
    }

    return mars_dict