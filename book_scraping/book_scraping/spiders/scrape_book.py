import scrapy
from ..items import BookScrapingItem

class ScrapeBooks(scrapy.Spider):
    name = 'scrape_books'

    page_number = 2

    start_urls = [
            "https://www.flipkart.com/books/economics-business-and-management-books/pr?sid=bks,xjk&marketplace=FLIPKART&otracker=nmenu_sub_Sports%2C%20Books%20%26%20More_0_Business&page=1"

    ]

    def parse(self, response):
        items = BookScrapingItem()

        all_books = response.css("._3liAhj")

        for div in all_books:
            book_name = div.css("._2cLu-l::text").extract()
            book_price = div.css("._1vC4OE::text").extract()
            book_rating = div.css(".hGSR34::text").extract()

            items['book_name'] = book_name
            items['book_price'] = book_price
            items['book_rating'] = book_rating

            yield items

        next_page = "https://www.flipkart.com/books/economics-business-and-management-books/pr?sid=bks,xjk&marketplace=FLIPKART&otracker=nmenu_sub_Sports%2C%20Books%20%26%20More_0_Business&page="+str(ScrapeBooks.page_number)

        if ScrapeBooks.page_number <= 20:
            ScrapeBooks.page_number += 1
            yield response.follow(next_page, callback=self.parse)

