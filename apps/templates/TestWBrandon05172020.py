# Visit the mars nasa news site
browser = Browser("chrome", executable_path=r"\Users\dcohen\Documents\UCBE\Mission-to-Mars\apps\chromedriver.exe", headless=True)
#browser = Browser('chrome', **executable_path, headless=False)
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
    slide_elem.find("div", class_="content_title")
    # Use the parent element to find the first 'a' tag and save it as 'news_title'
    news_title = slide_elem.find("div", class_="content_title").get_text()
    # Use the parent element to find the paragraph text
    news_paragraph = slide_elem.find("div", class_="article_teaser_body").get_text()
except AttributeError:
    return None
print('news_title', news_title, 'news_paragraph', news_paragraph)
