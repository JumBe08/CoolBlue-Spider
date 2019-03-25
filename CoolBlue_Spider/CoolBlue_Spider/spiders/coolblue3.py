import scrapy
from ..items import CoolBlueItems

# I used this code to test the filtering that the spider was applying when scraping coolblue. If i only leave the
# no filter option in the last request i got the same results and less requests compared to the situation where i used
# that option in all of the requests

class QuoteSpider(scrapy.Spider):

    name = "coolblue3"
    start_urls = [
    #   "https://www.coolblue.nl/en/printers-scanners"
    #   "https://www.coolblue.nl/en/laptops-desktops-monitors"
    #     "https://www.coolblue.nl/en/peripherals"
    # "https://www.coolblue.nl/en/computer-parts"
    # "https://www.coolblue.nl/en/gaming"
        "https://www.coolblue.nl/en/laptops?page=1"
    ]

    def __init__(self):

        self.declare_xpath()

    # I'll declare all the xpaths I need here
    # def declare_xpath(self):
    #
    #     # There are links to category pages at the start url that we will scrap, because some category pages, like
    #     # "Store and preserve" for example, only show up here
    #     self.get_Category_links = "//a[@class='category-navigation--link']/@href"
    #
    #     # This will point to all the category section's headers at start url. For example:
    #     #       - Laptops, Desktops and Monitors
    #     #       - Peripherals
    #     #       - Television & Projectors
    #     #       - ..
    #     self.get_Category_Navigation_Links = "//h3[@class='product-category-navigation__title']/a/@href"
    #
    #     # I am scraping the categories in the grid as well as the indexed ones, just to make sure I'm not missing
    #     # anything. Some categories that are missing if i didn't scrap this field:
    #     #   - screen-protectors-for-ereaders
    #     #   -/en/software/office-software
    #     self.get_Grid_Links = "//a[@class='visual-entrance-card text-align--center js-visual-entrance-card']/@href"
    #
    #     # These pages are category sections. It has a catalog of available categories, which we will scrap.
    #     # For example, one of these pages is: https://www.coolblue.nl/en/laptops-desktops-monitors
    #     # Some of the categories listed here are:
    #     #       - Desktop PCs
    #     #       - Laptops
    #     #       - ..
    #     self.get_Indexed_Links = "//li[@class='indexed-link-list__item']/a/@href"
    #
    #     # I'll use this variable to differentiate a page with a list of products from a category page, who lacks this
    #     # div tag
    #     self.check_type_page = "//div[@class='js-products-component']"
    #
    #     # This will get the products' urls
    #     self.get_Product_Links = "//a[@class='product__image-link']/@href"
    #
    #     # Most of the times when im parsing product pages im expecting a complete url at a specific href value I'm
    #     # extracting. Sometimes, only part of the url is present, for example the second chance products. There might
    #     # be others that I'm also not aware, so ill make sure I can recognize in order to call .urljoin
    #     self.Check_Complete_Url = "https://www.coolblue.nl"
    #
    #     self.next_page_link = "//a[@class='pagination__link  js-pagination-item']/@href"
    #
    #     # Path to PRODUCT URL inside a given PRODUCT PAGE
    #     self.product_url = "//link[@rel='canonical']/@href"
    #
    #     # I'll also scrap second chance products when they are available at a given product's page
    #     self.direct_second_chance_link = "//a[@class='link-with-price']/@href"
    #
    #     # Products at the SECOND CHANCE CATEGORY have a different path to the URL
    #     self.second_chance_product_url = "//input[@type='hidden']/@value"
    #
    #     # I need to recognize when I am parsing a SECOND CHANCE PRODUCT in order to choose the correct PATH
    #     self.check_second_chance_url = "en/second-chance-product/"
    #
    #     # Path to PRODUCT PRICE inside a given PRODUCT PAGE
    #     self.product_price = "//div[@class='product-order']//span[@class='sales-price__former']/text()"
    #     #
    #     # # Path to PRODUCT PROMOTIONAL PRICE inside a given PRODUCT PAGE
    #     self.product_promotional_price = "//div[@class='product-order']//strong[@class='sales-price__current']/text()"
    #
    # def parse(self, response):
    #
    #     #   Here we are at a CATEGORY SECTION and we are selecting CATEGORIES from the GRID
    #     for category_link in response.xpath(self.get_Grid_Links).getall():
    #
    #         url = response.urljoin(category_link)
    #
    #         # I need to set dont't_filter to true, so that the request can track all the subcategories
    #         yield scrapy.Request(url=url, callback=self.parse_product_page)
    #
    # #   Here we are at a CATEGORY SECTION and we are selecting CATEGORIES from the INDEX
    #     for category_link in response.xpath(self.get_Indexed_Links).getall():
    #
    #         url = response.urljoin(category_link)
    #
    #         yield scrapy.Request(url=url, callback=self.parse_product_page)
    #
    # def parse_product_page(self, response):
    #
    #     # If the result of this condition is True, then we must be in a page with a list of categories and we need to
    #     # call parse_category_navigation again
    #     if response.xpath(self.check_type_page) == []:
    #
    #         yield scrapy.Request(url=response.url, callback=self.parse, dont_filter=True)
    #
    #     else:
    #
    #         # item = CoolBlueItems()
    #         #
    #         # item["Url"] = response.url
    #         #
    #         # yield item
    #
    #         for product_link in response.xpath(self.get_Product_Links).getall():
    #
    #             # Here I am checking if "https://www.coolblue.nl" in the field with the url. If it is, then it's a full
    #             # url. If it is not then I'll call .urljoin
    #             if self.Check_Complete_Url in product_link:
    #
    #                 url = product_link
    #
    #                 yield scrapy.Request(url=url, callback=self.parse_product)
    #
    #             else:
    #
    #                 url = response.urljoin(product_link)
    #
    #                 yield scrapy.Request(url=url, callback=self.parse_product)
    #
    #             next_page = response.xpath(self.next_page_link).get()
    #
    #             if next_page is not None:
    #                 url = response.urljoin(next_page)
    #
    #                 yield scrapy.Request(url=url, callback=self.parse_product_page)
    #
    #             # # SAVING THIS FOR DEBUGGING
    #             # item = CoolBlueItems()
    #             #
    #             # for product_link in response.xpath(self.get_Product_Links).getall():
    #             #
    #             #     if self.Check_Complete_Url in product_link:
    #             #
    #             #         item["Url"] = product_link
    #             #
    #             #         yield item
    #             #
    #             #     else:
    #             #
    #             #         item["Url"] = response.urljoin(product_link)
    #             #
    #             #         yield item
    #             #
    #             #     next_page = response.xpath(self.next_page_link).get()
    #             #
    #             #     if next_page is not None:
    #             #
    #             #         url = response.urljoin(next_page)
    #             #
    #             #         yield scrapy.Request(url=url, callback=self.parse_product_page)
    #
    #             #####################
    #
    #             # item = CoolBlueItems()
    #             #
    #             # item["Url"] = response.url
    #             #
    #             # yield item
    # # At a product's page we will parse the URL, the price and the promotional price. We will also parse
    # # any second chance offers, if available
    # def parse_product(self, response):
    #
    #     # We check if the path for a second chance offer is not empty. If it is not, then there is indeed a
    #     # second chance offer that we are going to scrap. If it is empty we parse the item normally and move on
    #     if response.xpath(self.direct_second_chance_link) != []:
    #
    #         url = response.urljoin(response.xpath(self.direct_second_chance_link).get())
    #
    #         yield scrapy.Request(url=url, callback=self.parse_product, dont_filter=True)
    #
    #     item = CoolBlueItems()
    #
    #     if self.check_second_chance_url in response.url:
    #
    #         item["Url"] = response.xpath(self.second_chance_product_url).get()
    #
    #         price = response.xpath(self.product_price).get()
    #
    #         # Second chance product prices' text starts with the string "Purchase price " and only then it prints the
    #         # actual price. I only want the numbers in the .csv, so I am cleaning the string
    #         item["Price"] = price.replace("Purchase price ", "")
    #
    #     else:
    #
    #         item["Url"] = response.xpath(self.product_url).get()
    #
    #         item["Price"] = response.xpath(self.product_price).get()
    #
    #     item["Promotional_Price"] = response.xpath(self.product_promotional_price).get()
    #
    #     # Seems like because of the yield that I am already using in this function I'm also forced to use yield
    #     # to get the items, instead of return, which won't return anything at all, even though all the code
    #     # runs fine up until this point


    def declare_xpath(self):

        # These links get information from the ASSORTMENT PAGE:
        #
        #   - get_Category_Navigation_Links: These always lead to pages with a list of subcategories
        #       Examples:   - Laptops, desktops, monitors
        #                   - Home cinema
        #
        #   - get_Category_links: Links to subcategories. Most of the times they lead to pages with a list
        #   of products (for example, "Laptops" and "Consoles"). Rarely, they'll lead to a page with a list
        #   of more subcategories (for example, "Office Supplies" and "Toner Cartridges"
        #       Examples of links that lead to pages with products listings:
        #           - Laptops
        #           - Consoles
        #       Examples of links that lead to pages with subcategories listings:
        #           - Office Supplies
        #           - Toner Cartridges

        self.get_Category_Navigation_Links = "//h3[@class='product-category-navigation__title']/a/@href"

        self.get_Category_Links = "//a[@class='category-navigation--link']/@href"

        # These links get information from pages with SUBCATEGORIES LISTS. Many categories are listed in the
        # assortment page, but not all of them, so we are checking these pages for missing subcategories.
        # These pages have 2 sections with links, the Grid and the Index

        self.get_Grid_Links = "//a[@class='visual-entrance-card text-align--center js-visual-entrance-card']/@href"

        self.get_Indexed_Links = "//li[@class='indexed-link-list__item']/a/@href"

        # I'll use this variable to differentiate a page with a list of products from a category page, which
        # lacks this "div" tag
        self.check_type_page = "//div[@class='js-products-component']"

        # Most of the times when im parsing product pages im expecting a complete url at a specific href value I'm
        # extracting. Sometimes, only part of the url is present, for example the second chance products. There might
        # be others that I'm also not aware, so ill make sure I can recognize in order to call .urljoin
        self.Check_Product_Complete_Url = "https://www.coolblue.nl"

        self.get_Product_Links = "//a[@class='product__image-link']/@href"

        self.next_page_link = "//a[@class='pagination__link  js-pagination-item']/@href"

        # Path to PRODUCT URL inside a given PRODUCT PAGE
        self.product_url = "//link[@rel='canonical']/@href"

        # I'll also scrap second chance products when they are available at a given product's page
        self.direct_second_chance_link = "//a[@class='link-with-price']/@href"

        # Products at the SECOND CHANCE CATEGORY have a different path to the URL
        self.second_chance_product_url = "//input[@type='hidden']/@value"

        # I need to recognize when I am parsing a SECOND CHANCE PRODUCT in order to choose the correct PATH
        self.check_second_chance_url = "en/second-chance-product/"

        # Path to PRODUCT PRICE inside a given PRODUCT PAGE
        self.product_price = "//div[@class='product-order']//span[@class='sales-price__former']/text()"
        #
        # # Path to PRODUCT PROMOTIONAL PRICE inside a given PRODUCT PAGE
        self.product_promotional_price = "//div[@class='product-order']//strong[@class='sales-price__current']/text()"


    def parse(self, response):

        for product_link in response.xpath(self.get_Product_Links).getall():

            url = response.urljoin(product_link)

            yield scrapy.Request(url=url, callback=self.parse_product)

        next_page = response.xpath(self.next_page_link).get()

        if next_page is not None:

            url = response.urljoin(next_page)

            yield scrapy.Request(url=url, callback=self.parse)


    def parse_product(self, response):

        item = CoolBlueItems()

        if self.check_second_chance_url in response.url:

            item["Url"] = response.xpath(self.second_chance_product_url).get()

            price = response.xpath(self.product_price).get()

            # Second chance product prices' text starts with the string "Purchase price " and only then it prints the
            # actual price. I only want the numbers in the .csv, so I am cleaning the string
            item["Price"] = price.replace("Purchase price ", "")

        else:

            item["Url"] = response.xpath(self.product_url).get()

            item["Price"] = response.xpath(self.product_price).get()

        item["Promotional_Price"] = response.xpath(self.product_promotional_price).get()

        return item
