# Import Splinter & BeautifulSoup, set the executable path, and initialize the chrome browser in Splinter.

from splinter import Browser
executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path, headless=True)
from bs4 import BeautifulSoup

# Define the "scrape_all" function.
def scrape_all():
    # Initiate headless driver for deployment.
    browser = Browser("chrome", executable_path="chromedriver", headless=True)

    # Set news title & paragraph variables.
    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions & store results in a dictionary.
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now()
    }

# Adding "mars_news" function.
def mars_news(browser):

    # Visit the mars NASA news site.
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    #   Optional delay for loading the page.
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    html = browser.html
    news_soup = BeautifulSoup(html, 'html.parser')

    # Add try/except for error-handling.
    try:
        slide_elem = news_soup.select_one('ul.item_list li.slide')

        slide_elem.find("div", class_='content_title')

        # Use the parent element to find the 1st 'a' tag and save as "news_title."
        news_title = slide_elem.find('div', class_='content_title').get_text()

        # Use the parent element to find the summary of the most recent article using find().
        news_p = slide_elem.find('div', class_="article_teaser_body").get_text()

    except AttributeError:
        return None, None

    return news_title, news_p

# Scrape the featured image.
def featured_image(browser):
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

# Add try/except for error handling.
    try:
        # Find the full-size image URL. 
        img_url = img_soup.select_one('figure.lede a img').get("src")
    
    except AttributeError:
        return None

    #return img_url        

    # Complete the URL.
    img_url = f'https://www.jpl.nasa.gov{img_url}'
    return img_url

# Scrape the "MARS PLANET PROFILE" table with Pandas.

import pandas as pd

def mars_facts():
    try: 
        # Create a DataFrame for the "MARS PLANET PROFILE" table info.
        df = pd.read_html('http://space-facts.com/mars/')[0]

    except BaseException:
        return None    
    
    # Assign columns & set DataFrame index.
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)
    df

    # Convert the DataFrame back into HTML.
    return df.to_html()

# Run the code.
if __name__ == "__main__":
    print(scrape_all())

# Properly end the automated browsing session.
browser.quit()