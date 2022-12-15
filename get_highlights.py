# Inspired by looking at below article.
# https://medium.com/@meeusdylan/extracting-kindle-highlights-1e5308fcda77
# Resolved some of the issues facing with the scripts mentioned.
# Currently repo's mentioned in that page seems to be not available.
# This can be further improved 
# Syntax: python get_highlights.py <kindle-username> <kindle-password>
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import json
import time
import sys

def login(web):
    #web.go_to(url)
    #up = extractUserPass()
    #web.implicitly_wait(10)
    time.sleep(3)
    up = (sys.argv[1], sys.argv[2])
    
    username = web.find_element(By.ID, 'ap_email')
    password = web.find_element(By.ID, 'ap_password')

    username.send_keys(up[0])
    password.send_keys(up[1])
    password.send_keys(Keys.ENTER)
	
def extractBooks(web):
    books = web.find_elements(By.TAG_NAME, 'h2')
    #books = []
    #for h in h2s:
    #    books.append(h.text)
    return books


def extractHighlights(web, book):
    #web.click(book)
    book.click()
    time.sleep(5)
    elements = web.find_elements(By.ID, 'highlight')
    highlights = []
    for e in elements:
        #print("==================")
        print(e.text)
        highlights.append(e.text)
    return highlights	



if __name__ == '__main__':
    #web = Browser(showWindow=True) # easier debugging
    web = webdriver.Chrome('./chromedriver')
    web.get("https://read.amazon.com/notebook")
    login(web)
    web.get("https://read.amazon.com/notebook")
    time.sleep(5)
    books = extractBooks(web)
    book_highlights = {}
    for book in books[:]:
        title = book.text
        print("extracting highlights for " + str(title))
        try:
            hs = extractHighlights(web, book)
            if hs:
                book_highlights[title] = hs
        except Exception as e:
            print("could not extract highlights for: " + str(title))
            print("exception: ", e)
            sys.exit(1)
    print("writing to json file")
    js = json.dumps(book_highlights)
    f = open("kindle-books-highlights.json", 'w')
    f.write(js)
    f.close()
    print("done")