# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import mysql.connector

class BookScrapingPipeline(object):

    def __init__(self):
        self.create_connector()
        self.create_table()        

    def create_connector(self):
        self.conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            passwd = '',
            database = 'ScrapeBooks'
        )

        self.curr = self.conn.cursor()

    def create_table(self):
        self.curr.execute("""DROP TABLE IF EXISTS scraped_books""")
        self.curr.execute(""" CREATE TABLE scraped_books(
            book_name TEXT,
            book_price INT,
            book_rating DOUBLE
        )""")

    def process_item(self, item, spider):
        self.store_db(item)
        return item

    def store_db(self, item):
        self.curr.execute("""INSERT INTO scraped_books VALUES (%s,%s,%s)""",(
            item['book_name'][0],
            item['book_price'][0][1:],
            item['book_rating'][0]
        ))

        self.conn.commit()