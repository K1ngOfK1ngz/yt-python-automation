#!/usr/bin/python3

import requests
import os
import sys
from bs4 import BeautifulSoup

URL = "https://www.imdb.com/chart/top/?ref_=nv_mv_250"
HEADERS = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"}

page = requests.get(URL, headers=HEADERS)
#print(page)

if page.status_code != 200:
    print("Unable to find URL")
else:
    soup = BeautifulSoup(page.content, "html.parser")
    #titles = soup.find_all('div', {'class' : 'ipc-title ipc-title--base ipc-title--title ipc-title-link-no-icon ipc-title--on-textPrimary sc-14dd939d-7 fjdYTb cli-title'})
    titles = soup.find_all('div', {'class' : 'ipc-title ipc-title--base ipc-title--title ipc-title-link-no-icon ipc-title--on-textPrimary sc-be6f1408-9 srahg cli-title'})
    
    base_url = "https://www.imdb.com"
    for title in titles:
        # Strip the number ranking out of the title
        movie_title = title.a.text.split(".", 1)[1].strip()
        try:
            # Get title only by pulling out the a tag and create a file name in a directory called Reviews
            f = open("Reviews/" + movie_title, 'w')
        except FileNotFoundError:
            # Directory not found, create Directory first
            os.mkdir("Reviews")
            f = open("Reviews/%s" % movie_title, 'w')
        
        movie_details_url = "{}{}".format(base_url, title.a['href'])
        movie_page = requests.get(movie_details_url, headers=HEADERS)
        soup = BeautifulSoup(movie_page.content, "html.parser")
        
        # Find the User reviews href
        ipc_link = soup.find_all('a', {'class' : 'ipc-link ipc-link--baseAlt ipc-link--inherit-color'})
        for r in ipc_link:
            if r.text == "User reviews":
                review_link = r['href']
        
        # Navigate to Movie title's review page
        all_reviews_page = requests.get("{}/{}".format(base_url, review_link))
        soup = BeautifulSoup(all_reviews_page.content, "html.parser")
        reviews = soup.find_all('div', {'class' : 'text show-more__control'})
        
        print('Recording reviews for {}...'.format(movie_title))
        for review in reviews:
            comment = review.text
            f.write(comment + "\n")
        f.close()
        