#include important libraries
import json
import requests
from bs4 import BeautifulSoup
import pymongo


#encapsulate web crawling functionalities
class Crawler():
    #start_url = 'https://eosyqwa4e840ueb.m.pipedream.net'

    connection = 'mongodb+srv://bhadoria1923:bhadoria1923@cluster0.b8ruxqv.mongodb.net/PB_Search_engine?retryWrites=true&w=majority'

    client = pymongo.MongoClient(connection)

    db = client.PB_Search_engine

    text_tags = ['p','h','div']
    search_results = []
    def crawl(self,url,depth):
        try:
            print('crawling url: "%s"  at depth: "%d"' % (url,depth))
            response = requests.get(url,headers={'user-agent': 'PB-Search'})

        except:
            print('failed to perform get request on "%s"' % url)
            return

        content = BeautifulSoup(response.text,'lxml')

        #links = content.findAll('a')
        try:
            title = content.find('title').text
            description = ''
            for tag in content.findAll():
                if tag.name in self.text_tags:
                    description += tag.text.strip().replace('/n', '')

        except:
            return



        result={
            'url' : url,
            'title' : title,
            'description' : description
            }

        search_results = self.db.search_results
        search_results.insert_one(result)
        search_results.create_index([
            ('url', pymongo.TEXT),
            ('title', pymongo.TEXT),
            ('description', pymongo.TEXT)
        ], name='search_results', default_language='english')

        self.search_results.append(result)
        #print(json.dumps(result,indent=2))

        #print('\n\n Return:', json.dumps(result, indent=2 ))

        if depth == 0:
            return #result

        links = content.findAll('a')



        for link in links:
            try:
                if 'http' in link['href']:
                    self.crawl(self,link['href'], depth - 1)
            except KeyError:
                pass

        self.client.close()



Crawler.crawl(Crawler,'https://stackoverflow.com/questions?tab=newest&page=2', 5)

#Crawler.print_data(Crawler)

print('length of data:',len(Crawler.search_results))
