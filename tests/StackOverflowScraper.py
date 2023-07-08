#
# StackOverflow questions scraper
#

# import necessary libraries
import json
import requests
from bs4 import BeautifulSoup

# Base Url
start_url = 'https://stackoverflow.com/questions?tab=newest&page='

# Loop over questions' pages of StackOverflow
for pg_no in range(1,100):

    # next url
    url = start_url+str(pg_no)

    # make http get request to the given url
    response = requests.get(url)

    # parse the content
    content = BeautifulSoup(response.text,'lxml')

    # extract the links
    links = content.findAll('a',{'class': 's-link'})

    # extract description of questions
    descriptions = content.findAll('div',{'class':'s-post-summary--content-excerpt'})

    print('\n\nURL:', url)

    for index in range(0,len(descriptions)):
        # store items in dictionary
        question = {
            'title': links[index].text,
            'url': links[index]['href'],
            'description': descriptions[index].text.strip().replace('\n','')
        }
        print(json.dumps(question,indent=2))


