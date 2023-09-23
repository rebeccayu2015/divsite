from selenium import webdriver
from bs4 import BeautifulSoup

googleURL = "https://dining.columbia.edu/content/jjs-place-0"

browser = webdriver.Firefox()
browser.get(googleURL)
content = browser.page_source

soup = BeautifulSoup(content)

print(soup)
