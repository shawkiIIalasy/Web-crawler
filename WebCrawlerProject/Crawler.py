from crawlerFunction import *
from urllib.request import urlopen
from filterHtml import *


class Crawler:
    project_name = ""
    base_url = ""
    main_url = ""
    queue = set()
    crawled = set()

    def __init__(self, project_name, main_url, base_url):
        Crawler.project_name = project_name
        Crawler.base_url = base_url
        Crawler.main_url = main_url
        self.boot()
        self.crawling("First Crawler",Crawler.base_url)

    def boot(self):
        create_data_file(Crawler.project_name,Crawler.base_url)
        Crawler.queue = merge_to_file('storage/' + Crawler.project_name + '/queue.txt')
        Crawler.crawled = merge_to_file('storage/' + Crawler.project_name + '/crawler.txt')

    @staticmethod
    def crawling(thread_name, url):
        if url not in Crawler.crawled:
            Crawler.add_links(Crawler.get_links(url))
            Crawler.queue.remove(url)
            Crawler.crawled.add(url)
            Crawler.update()

    @staticmethod
    def get_links(url):
        html_str = ""
        try:
            response = urlopen(url)
            if 'text/html' in response.getheader('Content-Type'):
                html_bytes = response.read()
                html_str = html_bytes.decode("utf-8")
            filter = filterHtml(Crawler.base_url, url)
            filter.feed(html_str)
        except Exception as e:
            return set()
        return filter.get_page_links()

    @staticmethod
    def add_links(links):
        for link in links:
            if (link in Crawler.queue )or (link in Crawler.crawled):
                continue

            if get_domain(Crawler.main_url) != get_domain(link):
                continue
            Crawler.queue.add(link)

    @staticmethod
    def update():
        update_file(Crawler.queue, 'storage/' + Crawler.project_name + '/queue.txt')
        update_file(Crawler.queue, 'storage/' + Crawler.project_name + '/crawler.txt')

