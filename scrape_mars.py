# Import Splinter & BeautifulSoup, set the executable path, and initialize the chrome browser in Splinter.

from splinter import Browser
executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)
from bs4 import BeautifulSoup

# Visit the mars NASA news site.
url = 'https://mars.nasa.gov/news/'
browser.visit(url)

# Optional delay for loading the page.
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

html = browser.html
news_soup = BeautifulSoup(html, 'html.parser')
slide_elem = news_soup.select_one('ul.item_list li.slide')

slide_elem.find("div", class_='content_title')

# Use the parent element to find the 1st 'a' tag and save as "news_title."
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title

# Use the parent element to find the summary of the most recent article using find().
news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
news_p

# Scrape the featured image.
url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)

# Find and click the FULL IMAGE button.
full_image_elem = browser.find_by_id('full_image')
full_image_elem.click()

# Find the "More Info" button and click it.
browser.is_element_present_by_text('more info', wait_time=1)
more_info_elem = browser.find_link_by_partial_text('more info')
more_info_elem.click()

# Parse the resulting HTML with BeautifulSoup.
html = browser.html
img_soup = BeautifulSoup(html, 'html.parser')

# Find the full-size image URL. 
img_url_rel = img_soup.select_one('figure.lede a img').get("src")
img_url_rel

# Complete the URL.
img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
img_url

# Scrape the "MARS PLANET PROFILE" table with Pandas.

import pandas as pd

# Create a DataFrame for the "MARS PLANET PROFILE" table info.
df = pd.read_html('http://space-facts.com/mars/')[0]
df.columns=['description', 'value']
df.set_index('description', inplace=True)
df

# Convert the DataFrame back into HTML.
df.to_html()

# Properly end the automated browsing session.
browser.quit()