
# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

def scrape_all():
    # Initiate headless driver for deployment
    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)
    hemisphere_image_urls = hemisphere(browser)

    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemispheres": hemisphere_image_urls,
        "last_modified": dt.datetime.now()
    }
    # Stop webdriver and return data
    browser.quit()
    return data


def mars_news(browser):

    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)



    # Parse the HTML, Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
         slide_elem = news_soup.select_one('div.list_text')
         slide_elem.find('div', class_='content_title')
         # Use the parent element to find the first `a` tag and save it as `news_title`
         news_title = slide_elem.find('div', class_='content_title').get_text()
         # Use the parent element to find the paragraph text
         news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    except AttributeError:
        return None, None

    return news_title, news_p

# ### Featured Images
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
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    return img_url


#creating a new DataFrame from the HTML table. The Pandas function read_html()## Mars Facts
def mars_facts():
    # Add try/except for error handling
    try:
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    except Exception as x:
        print("Exception no good" + str(x))
        return None

    #assign columns to the new DataFrame
    df.columns=['description', 'Mars', 'Earth']
    #turning the Description column into the DataFrame's index
    df.set_index('description', inplace=True)



#convert our DataFrame back into HTML-ready code
    return df.to_html(classes="table table-striped")


#create a function that will scrape the hemisphere data, code from the Mission_to_Mars_Challenge.py
def hemisphere(browser):
    # 1. Use browser to visit the URL
    url = 'https://marshemispheres.com/'
    browser.visit(url)
    browser.is_element_present_by_css('div.list_text', wait_time=1)
    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    for x in range(4):
        hemispheres = {}
        try:
            browser.find_by_css("a.product-item h3")[x].click()

        except BaseException:
            print(f'Bad img_url link {hemisphere_image_urls}...try again', end='')

        sample_elem = browser.links.find_by_text('Sample').first

        hemispheres['img_url'] = sample_elem['href']

        title = browser.find_by_css("h2").text
        hemispheres["title"] = title
        hemisphere_image_urls.append(hemispheres)

        browser.back()
    return hemisphere_image_urls



#end the automated browsing session.
#browser.quit()

if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())




