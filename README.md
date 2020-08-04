# Web Scraping  - Mission to Mars

In this project, I built a web application that scrapes various websites for data related to Mars and displays the information in a single HTML page using FLASK. I used a MondoDB and performed basic CRUD operations like storing data, updating or overwriting the existing document each time new data is obtained. 

# Step 1 - Scraping

Using a web crawler like Splinter to navigate sites and Beautiful soup to parse data, I scraped multiple websites and stored the result in a Pandas dataframe and store the data to a MongoDB database.

The following are the websites I scraped -

# NASA Mars News
Scraped the NASA Mars News Site(https://mars.nasa.gov/news/) and collected the latest News Title and Paragraph Text. 

# JPL Mars Space Images - Featured Image
Visited the url for JPL Featured Space Image(https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars) to find the image url for the current Featured Mars Image
using Splinter to navigate the site.

# Mars Weather

* Visited the Mars Weather twitter account(https://twitter.com/marswxreport?lang=en) and scraped the latest Mars weather tweet from the page and saved the tweet text for the weather report as a variable called `mars_weather`.

# Mars Facts

* Visited the Mars Facts webpage(https://space-facts.com/mars/) and used Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.I then used Pandas to convert the data to a HTML table string.

# Mars Hemispheres

* Visited the USGS Astrogeology site (https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars) to obtain high resolution images for each of Mars hemispheres.
* Scraped both the image url string for the full resolution hemisphere image, and the Hemisphere title containing the hemisphere name.
* I stored the scraped data as a Python dictionary to store the data using the keys `img_url` and `title`. 
* Appended the dictionary with the image url string and the hemisphere title to a list. 

# Step 2 - MongoDB and Flask Application

I used MongoDB with Flask template to create a new HTML page that displays all of the information that was scraped from the URLs above.

* I created a Python script called `scrape_mars.py` with a function called `scrape` that executed all scraping code from above and returned one Python dictionary containing all of the scraped data.
* Next, I created a route called `/scrape` that imported the `scrape_mars.py` script and called the `scrape` function.
* Store the return value in Mongo as a Python dictionary.
* I created a root route `/` that queried the Mongo database and passed the mars data into an HTML template to display the data.
* I created a template HTML file called `index.html` that took the mars data dictionary and displayed all of the data in the appropriate HTML elements. 



