import scrapy
from ..items import CoolBlueItems


class QuoteSpider(scrapy.Spider):

    name = "coolblue2"

    start_urls = [
        "https://www.coolblue.nl/en/our-assortment"
    ]

    def __init__(self):

        self.declare_xpath()

    # I'll declare all the xpaths I need here
    def declare_xpath(self):

        # There are links to category pages at the start url that we will scrap, because some category pages, like
        # "Store and preserve" for example, only show up here
        self.get_Category_links = "//a[@class='category-navigation--link']/@href"

        # This will point to all the category section's headers at start url. For example:
        #       - Laptops, Desktops and Monitors
        #       - Peripherals
        #       - Television & Projectors
        #       - ..
        self.get_Category_Navigation_Links = "//h3[@class='product-category-navigation__title']/a/@href"

        # I am scraping the categories in the grid as well as the indexed ones, just to make sure I'm not missing
        # anything. Some categories that are missing if i didn't scrap this field:
        #   - screen-protectors-for-ereaders
        #   -/en/software/office-software
        self.get_Grid_Links = "//a[@class='visual-entrance-card text-align--center js-visual-entrance-card']/@href"

        # These pages are category sections. It has a catalog of available categories, which we will scrap.
        # For example, one of these pages is: https://www.coolblue.nl/en/laptops-desktops-monitors
        # Some of the categories listed here are:
        #       - Desktop PCs
        #       - Laptops
        #       - ..
        self.get_Indexed_Links = "//li[@class='indexed-link-list__item']/a/@href"

        # I'll use this variable to differentiate a page with a list of products from a category page, who lacks this
        # div tag
        self.check_type_page = "//div[@class='js-products-component']"

        # This will get the products' urls
        self.get_Product_Links = "//a[@class='product__image-link']/@href"

        # Most of the times when im parsing product pages im expecting a complete url at a specific href value I'm
        # extracting. Sometimes, only part of the url is present, for example the second chance products. There might
        # be others that I'm also not aware, so ill make sure I can recognize in order to call .urljoin
        self.Check_Complete_Url = "https://www.coolblue.nl"

        self.next_page_link = "//a[@class='pagination__link  js-pagination-item']/@href"

        # Path to PRODUCT URL inside a given PRODUCT PAGE
        self.product_url = "//link[@rel='canonical']/@href"

        # Products at the SECOND CHANCE CATEGORY have a different path to the URL
        self.second_chance_product_url = "//input[@type='hidden']/@value"

        # I need to recognize when I am parsing a SECOND CHANCE PRODUCT in order to choose the correct PATH
        self.check_second_chance_url = "en/second-chance-product/"

        # Path to PRODUCT PRICE inside a given PRODUCT PAGE
        self.product_price = "//div[@class='product-order']//span[@class='sales-price__former']/text()"
        #
        # # Path to PRODUCT PROMOTIONAL PRICE inside a given PRODUCT PAGE
        self.product_promotional_price = "//div[@class='product-order']//strong[@class='sales-price__current']/text()"

    # I'd like to make a function for all those for cycles im repeating throughout the code
    # def scrap_links(self, response, selector, callback_function):
    #
    #     for link in response.xpath(selector).getall():
    #
    #         self.url = response.urljoin(link)
    #
    #         return scrapy.Request(url=self.url, callback=callback_function)


    # Here we will first get all the links for category pages available at in start_url. Then we will get all the links
    # for the category section's respective pages, where more categories are listed
    def parse(self, response):

        #   Gets the links from CATEGORY PAGES in the starting url
        for category_link in response.xpath(self.get_Category_links).getall():

            url = response.urljoin(category_link)

            yield scrapy.Request(url=url, callback=self.parse_product_page)

    #   Gets the links to CATEGORY SECTIONS from the starting url
        for cat_nav in response.xpath(self.get_Category_Navigation_Links).getall():

            url = response.urljoin(cat_nav)

            yield scrapy.Request(url=url, callback=self.parse_category_navigation)

        # DEBUGGING CATEGORY LINKS FROM ASSORTMENT PAGE
        # item = CoolBlueItems()
        #
        # for category_link in response.xpath(self.get_Category_links).getall():
        #     item["Url"] = response.urljoin(category_link)
        #     yield item

    # Here I'll scrap all the product categories inside those category section's pages
    def parse_category_navigation(self, response):

        #   Here we are at a CATEGORY SECTION and we are selecting CATEGORIES from the GRID
        for category_link in response.xpath(self.get_Grid_Links).getall():

            url = response.urljoin(category_link)

            yield scrapy.Request(url=url, callback=self.parse_product_page)

    #   Here we are at a CATEGORY SECTION and we are selecting CATEGORIES from the INDEX
        for category_link in response.xpath(self.get_Indexed_Links).getall():

            url = response.urljoin(category_link)

            yield scrapy.Request(url=url, callback=self.parse_product_page)

        # DEBUGGING
        # item = CoolBlueItems()
        #
        # # CATEGORY LINKS FROM GRID
        # for category_link in response.xpath(self.get_Grid_Links).getall():
        #
        #     item["Url"] = response.urljoin(category_link)
        #
        #     yield item
        #
        # # CATEGORY LINK FROM INDEX
        # for category_link in response.xpath(self.get_Indexed_Links).getall():
        #
        #     item["Url"] = response.urljoin(category_link)
        #
        #     yield item

    # Here I'll parse all the PRODUCT PAGES for PRODUCT URLS

    # Usually when this functions is called we are at a page with a listing of products.
    # There might be the case though, that when this function is called we end up at a product subcategories page.
    # For example, if go to the category page "Printers & Scanners" in the assortment page, we will end up at its
    # product categories' page. Most of the categories lead to pages with a list of products, like the category
    # "Printers" in the grid view and "Scanners" in the index. However, if we choose "Cartridges" from the grid view, or
    # "Printer accessories" from the index, we will end up at another page with product categories organized in a grid
    # and in an index.
    # We need to recognize this in order to parse all available category pages correctly
    def parse_product_page(self, response):

        # If the result of this condition is True, then we must be in a page with a list of categories and we need to
        # call parse_category_navigation again
        if response.xpath(self.check_type_page) == []:

            # Here I need to set the "dont_filter" tag to true, so that the spider doesn't avoid going into
            # subcategories. For example, without it the program wouldn't scrape the categories at "Laptops, Desktops &
            # Monitors" -> "Software"
            yield scrapy.Request(url=response.url, callback=self.parse_category_navigation, dont_filter=True)

        else:

            for product_link in response.xpath(self.get_Product_Links).getall():

                # Most of the products href tag that I'm getting at this point have a complete URL, but some dont, so I
                # need to call .urljoin on those
                if self.Check_Complete_Url in product_link:

                    url = product_link

                    yield scrapy.Request(url=url, callback=self.parse_product)

                else:

                    url = response.urljoin(product_link)

                    yield scrapy.Request(url=url, callback=self.parse_product)

                next_page = response.xpath(self.next_page_link).get()

                if next_page is not None:

                    url = response.urljoin(next_page)

                    yield scrapy.Request(url=url, callback=self.parse_product_page)

            # # SAVING THIS FOR DEBUGGING
            # item = CoolBlueItems()
            #
            # for product_link in response.xpath(self.get_Product_Links).getall():
            #
            #     if self.Check_Complete_Url in product_link:
            #
            #         item["Url"] = product_link
            #
            #         yield item
            #
            #     else:
            #
            #         item["Url"] = response.urljoin(product_link)
            #
            #         yield item
            #
            #     next_page = response.xpath(self.next_page_link).get()
            #
            #     if next_page is not None:
            #
            #         url = response.urljoin(next_page)
            #
            #         yield scrapy.Request(url=url, callback=self.parse_product_page)

    #####################

            # item = CoolBlueItems()
            #
            # item["Url"] = response.url
            #
            # yield item

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
