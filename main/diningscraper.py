from selenium import webdriver
from bs4 import BeautifulSoup
from django.conf import settings
import json

# URL_list = ["https://dining.columbia.edu/content/jjs-place-0", "https://dining.columbia.edu/content/ferris-booth-commons-0",
#             "https://dining.columbia.edu/content/faculty-house-0", "https://dining.columbia.edu/chef-mikes"]
# URL_names = ["JJ's Place", "Ferris", "Faculty House", "Chef Mike's"]
# master = {}

# for url, name in zip(URL_list, URL_names):
#     driver = webdriver.Safari('/usr/bin/safaridriver')
#     driver.get(url)
#     content = driver.page_source
#     soup = BeautifulSoup(content, 'lxml')
#     meals = soup.find("div", {"id": "cu-dining-meals"})
#     dishes = soup.find_all("div", {"class": "meal-items"})
#     inventory = {}
#     for dish in dishes:
#         dish_div = (soup.find_all(
#             "div", {"class": "meal-item angular-animate ng-trans ng-trans-fade-down"}))
#         oatmeal = soup.find_all("h5", {"class": "meal-title"})
#         for oat in oatmeal:
#             inventory[f"{oat.text}"] = [0, 0,[], []]
#     master[name] = inventory
#     driver.close()

# j = 0
# files = ['jj.txt', 'ferris.txt', 'faculty.txt', 'mike.txt']

# for i in master:
#     with open("media/files/" + files[j], 'w') as file:
#         items = json.dumps(str(master[i]))
#         items = items.replace('\\', '')
#         file.write(items)
#         file.close()
#     j += 1

# f = open('media/files/faculty.txt', 'r')
# items = f.read()

# for i in range(0, len(items)):
#     if items[i] == '\'' and (items[i-1] == ' ' or items[i-1] == '{'or items[i+1] == ':'):
#         items = items[:i] + '"' + items[i+1:]
# print(items[1:len(items)-1])

# items = json.loads(items[1:len(items)-1])

# f.close()

# print(type(items))
# print(items["BBQ Salmon"])
