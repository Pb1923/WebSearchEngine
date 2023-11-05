import asyncio
import requests
from bs4 import BeautifulSoup
import pymongo

class Crawler():

    connection = 'mongodb+srv://bhadoria1923:bhadoria1923@cluster0.b8ruxqv.mongodb.net/search?retryWrites=true&w=majority'

    client = pymongo.MongoClient(connection)
    db = client.search
    text_tags = ['p', 'h', 'div']
    search_results = []
    queue = asyncio.Queue()

    @staticmethod
    async def crawl(url):
        try:
            print('crawling url: "%s"' % url)
            response = requests.get(url, headers={'user-agent': 'PB-Search'})
        except:
            print('failed to perform get request on "%s"' % url)
            return

        content = BeautifulSoup(response.text, 'lxml')
        try:
            title = content.find('title').text
            description = ''
            for tag in content.findAll():
                if tag.name in Crawler.text_tags:
                    description += tag.text.strip().replace('/n', '')
        except:
            return

        result = {
            'url': url,
            'title': title,
            'description': description
        }

        search_results = Crawler.db.search
        search_results.insert_one(result)
        search_results.create_index([
            ('url', pymongo.TEXT),
            ('title', pymongo.TEXT),
            ('description', pymongo.TEXT)
        ], name='search_results', default_language='english')

        Crawler.search_results.append(result)

        links = content.findAll('a')
        for link in links:
            try:
                if 'http' in link['href']:
                    url = link['href']
                    if url not in Crawler.search_results:
                        await Crawler.queue.put(url)
            except KeyError:
                pass

    @staticmethod
    async def process_queue():
        while not Crawler.queue.empty():
            url = await Crawler.queue.get()
            await Crawler.crawl(url)

    @staticmethod
    async def start():
        await Crawler.queue.put('https://stackoverflow.com/questions')  # Add the URLs to crawl to the queue
        tasks = [asyncio.create_task(Crawler.process_queue()) for _ in range(10)]  # Create 10 tasks for processing the queue
        while True:
            await asyncio.sleep(1)
            print('checking for new pages...')
            for url in Crawler.search_results:
                head = requests.head(url)
                if head.status_code == 200:
                    await Crawler.queue.put(url)

if __name__ == '__main__':
    asyncio.run(Crawler.start())
