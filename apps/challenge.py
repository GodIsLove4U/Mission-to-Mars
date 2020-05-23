from flask import Flask, render_template
from flask_pymongo import PyMongo
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import sys, traceback
import datetime as dt

# Windows users
#executable_path = {'executable_path': 'chromedriver.exe'}
#browser = Browser('chrome', **executable_path, headless=False)
#executable_path = {'executable_path':r'C:\Users\dcohen\Documents\UCBE\Mission-to-Mars\apps\chromedriver.exe'}
#browser = Browser('chrome', **executable_path, headless=False)

def scrape_all():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    # Initiate headless driver for deployment
    news_title, news_paragraph = mars_news(browser)
    feature_image = featured_image(browser)

    mars_hemisphere_list = list()
    names = ['Cerberus', 'Schiaparelli', 'Syrtis Major', 'Valles Marineris']
    for name in names:
        hemisphere_title, hemisphere_img_url = mars_hemispheres(browser, name)
        hemisphere_dict = {"title": hemisphere_title, "img_url": hemisphere_img_url}
        mars_hemisphere_list.append(hemisphere_dict)

    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": feature_image,
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemisphere_data": mars_hemisphere_list
    }
    browser.quit()
    return data

def mars_news(browser):
    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    
    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)
    
    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = BeautifulSoup(html, 'html.parser')
    
    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one("ul.item_list li.slide")
        #slide_elem.find("div", class_="content_title")
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find("div", class_="content_title").get_text()
        # Use the parent element to find the paragraph text
        news_paragraph = slide_elem.find("div", class_="article_teaser_body").get_text()
    except AttributeError:
        return None, None
    return news_title, news_paragraph

# ""### Featured Images"
# Visit URL
def featured_image(browser):
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_id('full_image')
    full_image_elem.click()

    # Find the more info button and click that
    #browser.is_element_present_by_text('more info', wait_time=1)
    #browser.click_link_by_partial_text('more info')
    more_info_btn = browser.find_link_by_partial_text('more info')
    more_info_btn.click()
    #more_info_elem = browser.find_link_by_partial_text('more info')
    #more_info_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = BeautifulSoup(html, 'html.parser')

    print(img_soup)
    try:
        img_url_rel = img_soup.select_one("figure.lede a img").get("src")
    
    except AttributeError:
        err_state = 'What is this!'
        return err_state
    # Use the base URL to create an absolute URL
    #img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
    img_url = f'https://www.jpl.nasa.gov/spaceimages/images/largesize/PIA16613_hires.jpg'
    return img_url

def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('http://space-facts.com/mars/')[0]
    
    except BaseException:
        return None
    
    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars']
    df.set_index('Description', inplace=True)
    
    # Convert dataframe into HTML format, add bootstrap
    return df.to_html()

def mars_hemispheres(browser, hemisphere_name):
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    browser.is_element_present_by_text(f'{hemisphere_name} Hemisphere Enhanced', wait_time=.5)
    browser.click_link_by_partial_text(f'{hemisphere_name} Hemisphere Enhanced')
    soup = BeautifulSoup(browser.html, 'html.parser')
    try:
        hemis_url = soup.select_one('img.wide-image').get('src')
        title = soup.select_one('h2.title').text
    except AttributeError:
        return None

    img_url = f'http://astrogeology.usgs.gov{hemis_url}'

    return title, img_url

   # hemi = []

if __name__ == "__main__":
    #If running as script, print scraped data
    print(scrape_all())
 #   print ("pass")


#hemispheres = {
 #"https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif": cerberus_enhanced,
 #"https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif": schiaparelli_enhanced,
 #"https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif": syrtis_major_enhanced,
 #"https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced": valles_marineris_enhanced
#}

#hemi = [{'img_url':"https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif", 'title': 'cerberus_enhanced'},
 #   {'img_url':"https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif", 'title': 'schiaparelli_enhanced'},
  #  {'img_url':"https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif", 'title': 'syrtis_major_enhanced'},
   # {'img_url':"https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced", 'title': 'valles_marineris_enhanced'},
    #]