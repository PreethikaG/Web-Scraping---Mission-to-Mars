#Import Dependencies

from bs4 import BeautifulSoup as bs 
from splinter import Browser
import requests
import pandas as pd
import time
import pymongo


# Chromedriver Initialization
def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=True)

# A master function that calls separate function to scrape data from each website
# mars_final_output is the dictionary of all scraped data that is stored to a mongo database

def scrape_data():
    browser = init_browser()
    mars_final_output = {}
    
    mars_news = scrape_mars_news(browser)

    mars_final_output['Mars_Title'] = mars_news[0]
    mars_final_output['Mars_Para'] = mars_news[1]

    mars_final_output['Mars_Featured_Image'] = mars_featured_image(browser)

    mars_final_output['Twitter_Weather'] = mars_weather(browser)

    mars_final_output['MarsFacts'] = mars_facts_scrape(browser)

    mars_final_output['MarsHemispheres'] = mars_hemispheres(browser)

#Establish Mongo db connection with db(mars_db) and collection(mars_collection)

    conn = "mongodb://localhost:27017"
    client = pymongo.MongoClient(conn)
    db = client.mars_db
    collection = db.mars_collection

    collection.insert_one(mars_final_output)

    return mars_final_output



#function that scrapes latest mars news
def scrape_mars_news(browser):
           
    #Give url to scrap
    
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    time.sleep(2)
    html = browser.html
    soup = bs(html, 'html.parser')

    results = soup.find('li', class_='slide')
    
    news_para = results.find('div',class_="content_title").text
    news_title = results.find('div',class_="article_teaser_body").text
    print(news_para)
    print(news_title)
    output_news = [news_para,news_title]
    return output_news

#function that scrapes mars featured image
def mars_featured_image(browser):
    # browser = init_browser()

    imageurl = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(imageurl)
    
    html = browser.html
    soup = bs(html,'html.parser')

    browser.find_by_id('full_image').click()
    
    result_image = soup.find('a',class_="button fancybox")["data-fancybox-href"]
    print(result_image)

#Split the image url to get the first half of the url

    base_url = imageurl.split('/s',1)
    strip_url = base_url[0]
    strip_url

#Concatenate both the urls to get the featured image url
    image_url = strip_url+result_image
    image_url
    return(image_url)

#function that scrapes mars weather data from Twitter
def mars_weather(browser):
    # browser = init_browser()
    tweet_url="https://twitter.com/marswxreport?lang=en"
    browser.visit(tweet_url)
    time.sleep(5)
    html = browser.html
    soup = bs(html,'html.parser')

    time.sleep(5)
    tweets = soup.find('div', class_="css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0")

    for tweet in tweets:
        weather_data = tweets.text
        return(weather_data)

#function that scrapes mars facts and convert it to a dataframe
def mars_facts_scrape(browser):
    
    fact_url = "https://space-facts.com/mars/"

    mars_fact = pd.read_html(fact_url)
    mars_fact
    df_mars = mars_fact[0]
#Rename columns in dataframe, set index
    df_mars.columns = ['Description','Value']
    df_mars.set_index("Description",inplace=True)
    html_table=df_mars.to_html()
    final_table=html_table.replace('\n', '')
    return final_table

#function that scrapes images of hemispheres of mars

def mars_hemispheres(browser):
#Create a list "mars_hem" that stores te scraped data
    mars_hem = []

    hem_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    # spl_url = hem_url.split('/s',1)

    browser.visit(hem_url)
    html = browser.html
    soup = bs(html,'html.parser')
    results = soup.find_all('div',class_='description')
    for result in results:
    
        htag = result.find('h3')
        print(htag.text)
    
        next_link = result.find('a')['href']
        
        #Concatenate the two urls to go to the individual image page to scrape image url
        split_url = hem_url.split("/s")
        next_url_to_visit = split_url[0] + next_link
        
        browser.visit(next_url_to_visit)
        html=browser.html
        soup=bs(html,'html.parser')
    
        img_results = soup.find('div',class_='downloads')
        hreftag = img_results.find('a')['href']
        print(hreftag)

        mars_hem.append({"title" : htag.text, "img_url" : hreftag})
    
    return mars_hem


#scrape_data()