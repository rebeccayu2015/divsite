from django.shortcuts import render
from datetime import date
from selenium import webdriver
from bs4 import BeautifulSoup
from django.conf import settings
from django.contrib.auth.decorators import login_required
import json
from collections import OrderedDict
import numpy as np
from statistics import mean 

def scrape_dining():
    URL_list = ["https://dining.columbia.edu/content/jjs-place-0", "https://dining.columbia.edu/content/ferris-booth-commons-0",
                "https://dining.columbia.edu/content/faculty-house-0", "https://dining.columbia.edu/chef-mikes"]
    URL_names = ["JJ's Place", "Ferris", "Faculty House", "Chef Mike's"]
    master = {}

    for url, name in zip(URL_list, URL_names):
        driver = webdriver.Safari('/usr/bin/safaridriver')
        driver.get(url)
        content = driver.page_source
        soup = BeautifulSoup(content, 'lxml')
        meals = soup.find("div", {"id": "cu-dining-meals"})
        dishes = soup.find_all("div", {"class": "meal-items"})
        inventory = {}
        for dish in dishes:
            dish_div = (soup.find_all(
                "div", {"class": "meal-item angular-animate ng-trans ng-trans-fade-down"}))
            oatmeal = soup.find_all("h5", {"class": "meal-title"})
            for oat in oatmeal:
                inventory[f'{oat.text}'] = [0, 0, [], []]
        master[name] = inventory
        driver.close()

    j = 0
    files = ['jj.txt', 'ferris.txt', 'faculty.txt', 'mike.txt']

    for i in master:
        with open("media/files/" + files[j], 'w') as file:
            items = json.dumps(str(master[i]))
            items = items.replace('\\', '')
            file.write(items)
            file.close()
        j += 1

def read_file(file_name):
    f = open(file_name, 'r')
    items = f.read()

    for i in range(0, len(items)):
        if items[i] == '\'' and (items[i-1] == ' ' or items[i-1] == '{' or items[i+1] == ':'):
            items = items[:i] + '"' + items[i+1:]

    items = json.loads(items[1:len(items)-1])

    f.close()

    return items

def write_file(file_name, items):
    with open(file_name, 'w') as file:
        items = str(items)

        for i in range(0, len(items)):
            if items[i] == '\'' and (items[i-1] == ' ' or items[i-1] == '{' or items[i+1] == ':'):
                items = items[:i] + '"' + items[i+1:]

        items = items.replace('\\', '')

        if len(items) <= 2:
            items = "{'': [0, 0, [], []]}"
        file.write("\"" + items + "\"")
        file.close()

def get_avg(items):
    sum = 0
    count = 0
    for value in items.values():
        if value[1] != 0:
            sum += value[1]
            count += 1
    
    if sum == 0:
        return "N/A"

    return sum / count

# Create your views here.
def home(request):
    f = open('media/files/date.txt', 'r')
    curr_date = f.read()
    f.close()

    if curr_date != str(date.today()):
        scrape_dining()
        f = open('media/files/date.txt', 'w')
        f.write(str(date.today()))
        f.close()

    faculty_items = read_file('media/files/faculty.txt')
    faculty_items = dict(sorted(faculty_items.items(), key=lambda x: x[1], reverse=True))
    max_faculty = 0
    if (len(list(faculty_items)) > 0):
        max_faculty = faculty_items[list(faculty_items)[0]]

    ferris_items = read_file('media/files/ferris.txt')
    ferris_items = dict(sorted(ferris_items.items(), key=lambda x: x[1], reverse=True))
    max_ferris = 0
    if (len(list(faculty_items)) > 0):
        max_ferris = ferris_items[list(ferris_items)[0]]

    jj_items = read_file('media/files/jj.txt')
    jj_items = dict(sorted(jj_items.items(), key=lambda x: x[1], reverse=True))
    max_jj = 0
    if (len(list(jj_items)) > 0):
        max_jj = jj_items[list(jj_items)[0]]

    mike_items = read_file('media/files/mike.txt')
    mike_items = dict(sorted(mike_items.items(), key=lambda x: x[1], reverse=True))
    if (len(list(mike_items)) > 0):
        max_mike = mike_items[list(mike_items)[0]]

    # Best rated item
    best_rated = []
    if max_faculty[0] > max_ferris[0] and max_faculty[0] > max_jj[0] and max_faculty[0] > max_mike[0]:
        best_rated = ["Faculty House", list(faculty_items)[0], max_faculty[0], max_faculty[1]]
    elif max_ferris[0] > max_faculty[0] and max_ferris[0] > max_jj[0] and max_ferris[0] > max_mike[0]:
        best_rated = ["Ferris Booth Commons", list(ferris_items)[0], max_ferris[0], max_ferris[1]]
    elif max_jj[0] > max_faculty[0] and max_jj[0] > max_ferris[0] and max_jj[0] > max_mike[0]:
        best_rated = ["JJ's Place", list(jj_items)[0], max_jj[0], max_jj[1]]
    else:
        best_rated = ["Chef Mike's Sub Shop", list(mike_items)[0], max_mike[0], max_mike[1]]

    # Leaderboard
    highest_rated = [list(faculty_items)[0], list(ferris_items)[0], list(jj_items)[0], list(mike_items)[0]]

    avg_faculty = get_avg(faculty_items)
    avg_ferris = get_avg(ferris_items)
    avg_jj = get_avg(jj_items)
    avg_mike = get_avg(mike_items)
    avg_waits = [avg_faculty, avg_ferris, avg_jj, avg_mike]

    context = {
        'best_rated': best_rated,
        'highest_rated': highest_rated,
        'avg_waits': avg_waits
    }

    return render(request, 'main/home-page.html', context)

@login_required(login_url='/login/')
def faculty_house(request):
    items = read_file('media/files/faculty.txt')

    if request.method == "POST":
        if 'item' in request.POST:
            value = request.POST.get('item')
            value_split = value.split("_")
            item = value_split[0]
            reaction = value_split[1]

            if reaction == "like":
                items[item][0] += 1
            else:
                items[item][0] -= 1

            items[item][3].append(request.user.id)

            write_file('media/files/faculty.txt', items)
        if 'time-ranges' in request.POST:
            time_range = request.POST.get('time-ranges')
            time_range_split = time_range.split("_")
            item = time_range_split[0]
            time_range = int(time_range_split[1])

            if time_range != 0:
                items[item][2].append(time_range)
                avg_time = mean(items[item][2])
                items[item][1] = round(avg_time, 2)

                write_file('media/files/faculty.txt', items)

    items = dict(sorted(items.items(), key=lambda x: x[1], reverse=True))

    if items[list(items)[0]] == '':
        items = {}

    user=request.user
    context = {
        'item_info': items,
        'user': user,
    }

    return render(request, 'main/faculty.html', context)

@login_required(login_url='/login/')
def ferris_booth(request):
    items = read_file('media/files/ferris.txt')

    if request.method == "POST":
        if 'item' in request.POST:
            value = request.POST.get('item')
            value_split = value.split("_")
            item = value_split[0]
            reaction = value_split[1]

            if reaction == "like":
                items[item][0] += 1
            else:
                items[item][0] -= 1

            items[item][3].append(request.user.id)

            write_file('media/files/ferris.txt', items)
        if 'time-ranges' in request.POST:
            time_range = request.POST.get('time-ranges')
            time_range_split = time_range.split("_")
            item = time_range_split[0]
            time_range = int(time_range_split[1])

            if time_range != 0:
                items[item][2].append(time_range)
                avg_time = mean(items[item][2])
                items[item][1] = round(avg_time, 2)

                write_file('media/files/ferris.txt', items)

    items = dict(sorted(items.items(), key=lambda x: x[1], reverse=True))

    if items[list(items)[0]] == '':
        items = {}

    user=request.user
    context = {
        'item_info': items,
        'user': user,
    }

    return render(request, 'main/ferris.html', context)

@login_required(login_url='/login/')
def jj_place(request):
    items = read_file('media/files/jj.txt')

    if request.method == "POST":
        if 'item' in request.POST:
            value = request.POST.get('item')
            value_split = value.split("_")
            item = value_split[0]
            reaction = value_split[1]

            if reaction == "like":
                items[item][0] += 1
            else:
                items[item][0] -= 1

            items[item][3].append(request.user.id)

            write_file('media/files/jj.txt', items)
        if 'time-ranges' in request.POST:
            time_range = request.POST.get('time-ranges')
            time_range_split = time_range.split("_")
            item = time_range_split[0]
            time_range = int(time_range_split[1])

            if time_range != 0:
                items[item][2].append(time_range)
                avg_time = mean(items[item][2])
                items[item][1] = round(avg_time, 2)

                write_file('media/files/jj.txt', items)

    items = dict(sorted(items.items(), key=lambda x: x[1], reverse=True))

    if items[list(items)[0]] == '':
        items = {}

    user=request.user
    context = {
        'item_info': items,
        'user': user,
    }

    return render(request, 'main/jj.html', context)

@login_required(login_url='/login/')
def mike_sub(request):
    items = read_file('media/files/mike.txt')

    if request.method == "POST":
        if 'item' in request.POST:
            value = request.POST.get('item')
            value_split = value.split("_")
            item = value_split[0]
            reaction = value_split[1]

            if reaction == "like":
                items[item][0] += 1
            else:
                items[item][0] -= 1

            items[item][3].append(request.user.id)

            write_file('media/files/mike.txt', items)
        if 'time-ranges' in request.POST:
            time_range = request.POST.get('time-ranges')
            time_range_split = time_range.split("_")
            item = time_range_split[0]
            time_range = int(time_range_split[1])

            if time_range != 0:
                items[item][2].append(time_range)
                avg_time = mean(items[item][2])
                items[item][1] = round(avg_time, 2)

                write_file('media/files/mike.txt', items)

    items = dict(sorted(items.items(), key=lambda x: x[1], reverse=True))

    if list(items)[0] == '':
        items = {}

    user = request.user
    context = {
        'item_info': items,
        'user': user,
    }
    return render(request, 'main/mike.html', context)

