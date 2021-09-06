# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)

# Create variables for connection to website
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')

# Find website main elements to parse
slide_elem.find('div', class_='content_title')

# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()

# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

# ### Featured Images
# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)

# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')

# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'

# Read HTML data and create a DataFrame. Format index and columns
df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['Description', 'Mars', 'Earth']
df.set_index('Description', inplace=True)

# Convert DataFrame to HTML
df.to_html()

# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'
browser.visit(url)

# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# Retrieve html from webpage and parse with BeautifulSoup
html = browser.html
soup = soup(html, "html.parser")

# 3. Write code to retrieve the image urls and titles for each hemisphere.

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
temp_dict = dict(zip(title_list, photos_list))

# Append dictionary to hemisphere_image_urls
hemisphere_image_urls.append(temp_dict)

# 4. Print the list that holds the dictionary of each image url and title.
# hemisphere_image_urls

# 5. Quit the browser
browser.quit()


