import scrapy
from ..items import CoolBlueItems


class QuoteSpider(scrapy.Spider):

    name = "coolblue"
    start_urls = [
        "https://www.coolblue.nl/en/our-assortment"
    ]

    def __init__(self):

        self.declare_xpath()

    def declare_xpath(self):

        # These variables will get the links that lead to pages with lists of products, coming all the way from
        # the assortment page

        self.get_Category_Navigation_Links = "//h3[@class='product-category-navigation__title']/a/@href"

        self.get_Category_Links = "//a[@class='category-navigation--link']/@href"

        self.get_Grid_Links = "//a[@class='visual-entrance-card text-align--center js-visual-entrance-card']/@href"

        self.get_Indexed_Links = "//li[@class='indexed-link-list__item']/a/@href"

        ##############

        self.get_Product_Links = "//a[@class='product__image-link']/@href"

        self.next_page_link = "//a[@class='pagination__link  js-pagination-item']/@href"

        self.product_url = "//link[@rel='canonical']/@href"

        # Some products have a direct link to a second chance offer at their page which I'm going to use
        self.direct_second_chance_link = "//a[@class='link-with-price']/@href"

        # Second chance products have a different path to the URL
        self.second_chance_product_url = "//input[@type='hidden']/@value"

        # I need to recognize when I am parsing a second chance product in order to choose the correct path to
        # the URL
        self.check_second_chance_url = "en/second-chance-product/"

        self.product_price = "//div[@class='product-order']//span[@class='sales-price__former']/text()"

        self.product_promotional_price = "//div[@class='product-order']//strong[@class='sales-price__current']/text()"

    # This function processes:
    #   - Assortment page, which has links to subcategories pages and pages with lists of products
    #   - Subcategories pages (They only list more subcategories), which normally have a Grid and an Index
    #   - Pages with a list of products, which sometimes have an index with more subcategories
    def parse(self, response):

        if response.xpath(self.get_Category_Links):

            #   Gets links for subcategories from the assortment page
            for subcategory in response.xpath(self.get_Category_Links).getall():

                url = response.urljoin(subcategory)

                yield scrapy.Request(url=url, callback=self.parse)

        if response.xpath(self.get_Category_Navigation_Links):

            #   Gets links to subcategory sections from the assortment page
            for category_navigation in response.xpath(self.get_Category_Navigation_Links).getall():

                url = response.urljoin(category_navigation)

                yield scrapy.Request(url=url, callback=self.parse)

        if response.xpath(self.get_Indexed_Links):

            # Gets links to subcategories from the index, at a given subcategory page
            for subcategory in response.xpath(self.get_Indexed_Links).getall():

                url = response.urljoin(subcategory)

                yield scrapy.Request(url=url, callback=self.parse)

        if response.xpath(self.get_Grid_Links):

            # Gets links to subcategories from the grid, at a given subcategory page
            for subcategory in response.xpath(self.get_Grid_Links).getall():

                url = response.urljoin(subcategory)

                yield scrapy.Request(url=url, callback=self.parse)

        if response.xpath(self.get_Product_Links):

            for product_link in response.xpath(self.get_Product_Links).getall():

                url = response.urljoin(product_link)

                yield scrapy.Request(url=url, callback=self.parse_product)

            next_page = response.xpath(self.next_page_link).get()

            if next_page is not None:

                url = response.urljoin(next_page)

                yield scrapy.Request(url=url, callback=self.parse)

    def parse_product(self, response):

        item = CoolBlueItems()

        # Here I'm checking for second chance products while I'm at a product page
        second_chance_url = response.xpath(self.direct_second_chance_link).get()

        if second_chance_url:

            url = response.urljoin(second_chance_url)

            yield scrapy.Request(url=url, callback=self.parse_product)

        # Here I'm checking if I'm dealing with a second chance product, coming from a second chance subcategory
        # For example, in the assortment page, under promotions, there is a link to a Second Chance subcategories
        # There are more links like this one in other pages that I'm parsing.
        # We need to tell these products apart from the others, because we have to scrape their URLs and
        # Prices in a different way
        if self.check_second_chance_url in response.url:

            item["Url"] = response.xpath(self.second_chance_product_url).get()

            price = response.xpath(self.product_price).get()

            # Second chance product prices' text starts with the string "Purchase price " and only then it prints the
            # actual price. I only want the numbers in the .csv, so I am cleaning the string. Sometimes, the string
            # is missing.
            if "Purchase price " in price:

                item["Price"] = price.replace("Purchase price ", "")

            else:

                item["Price"] = price

        else:

            item["Url"] = response.xpath(self.product_url).get()

            item["Price"] = response.xpath(self.product_price).get()

        item["Promotional_Price"] = response.xpath(self.product_promotional_price).get()

        yield item
