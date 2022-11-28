#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests

def update_deadline():
    url = 'https://www.cshl.edu/education/undergraduate-research-program/#applying'
    r = requests.get(url, allow_redirects=True)
    open('test.html', 'wb').write(r.content)
    
    with open("test.html") as fp:
        soup = BeautifulSoup(fp, 'html.parser')
    
    text = soup.get_text()
    n = text.find('submitted')
    return text[n:n+30]





