import threading
from queue import Queue
from Crawler import *
from crawlerFunction import *


class CrawlerUrl:
    queue = Queue()
    project_name = ""
    queue_file = 'storage/' + project_name + '/queue.txt'
    crawled_file = 'storage/' + project_name + '/crawler.txt'
    number_of_threads = 10

    def __init__(self, project_name, url):
        CrawlerUrl.project_name = project_name
        CrawlerUrl.queue_file = 'storage/' + CrawlerUrl.project_name + '/queue.txt'
        CrawlerUrl.crawled_file = 'storage/' + CrawlerUrl.project_name + '/crawler.txt'
        Crawler(CrawlerUrl.project_name, url, url)
    def play(self):
        CrawlerUrl.create_workers()
        CrawlerUrl.crawl()
    @staticmethod
    def create_workers():
        for _ in range(CrawlerUrl.number_of_threads):
            t = threading.Thread(target=CrawlerUrl.work)
            t.daemon = True
            t.start()

    @staticmethod
    def work():
        while True:
            url = CrawlerUrl.queue.get()
            Crawler.crawling(threading.current_thread().name, url)
            CrawlerUrl.queue.task_done()

    @staticmethod
    def create_jobs():
        for link in merge_to_file(CrawlerUrl.queue_file):
            CrawlerUrl.queue.put(link)
        CrawlerUrl.queue.join()
        CrawlerUrl.crawl()

    # Check if there are items in the queue, if so crawl them
    @staticmethod
    def crawl():
        queued_links = merge_to_file(CrawlerUrl.queue_file)
        if len(queued_links) > 0:
            print(str(len(queued_links)) + ' links in the queue')
            CrawlerUrl.create_jobs()
