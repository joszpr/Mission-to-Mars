# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager

from Mission_to_Mars_Challenge import hemisphere_image_urls, title_list, photos_list


def scrape_all():
    # Set up Splinter & Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in dictionary
    data = {
          "news_title": news_title,
          "news_paragraph": news_paragraph,
          "featured_image": featured_image(browser),
          "facts": mars_facts(),
          "last_modified": dt.datetime.now(),
          "hemispheres": hemisphere_data(browser),
    }

    # Stop webdriver and return data
    browser.quit()
    return data

# Mars website function
def mars_news(browser):

    # Visit the Mars news site and Scrape
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        slide_elem.find('div', class_='content_title')

        # Use the parent element to find the first a tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()

        # Use the parent element to find the paragraph text
        news_paragraph = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    return news_title, news_paragraph

# ## JPL Space Images Featured Image

# Define Space Images function
def featured_image(browser):

    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base url to create an absolute url
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url


# ## Mars Hemisphere Images and Titles

# ## Mars Facts
# Define Mars website function
def mars_facts():

    try:
        # use 'read_html" to scrape the facts table into a dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns = ['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    return df.to_html()


# Define website function
def hemisphere_data(browser):

    # Use browser to visit the URL
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    # Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # Retrieve html from webpage and parse with BeautifulSoup
    # html = browser.html
    # soup = soup(html, "html.parser")

    # Create empty lists to place iteration values
    title_list = []
    photos_list = []

    # Find numbers of articles to iterate
    number_articles = len(browser.links.find_by_partial_text('Enhanced'))

    for x in range(0, number_articles):
        # Navigate browser to each article and append titles to a list
        browser.links.find_by_partial_text('Enhanced')[x].click()
        temp_title = browser.find_by_tag('h2')[0]
        title_list.append(temp_title.value)

        # Navigate browser to .jpg image and append link to a list
        browser.links.find_by_partial_text('Sample').click()
        temp_html = browser.windows[1].url
        photos_list.append(temp_html)

        # Close opened tab
        browser.windows[1].close()

        # Navigate browser to main page
        browser.back()

        continue

    # Convert lists into a dictionary
    hemisphere_image_urls.append({
        "img_url": photos_list,
        "title": title_list
    })

    return hemisphere_image_urls


if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())