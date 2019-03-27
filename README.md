# CoolBlue Spider

A spider to crawl the Website CoolBlue

HOW TO RUN  

Change directory to \CoolBlue-Spider\CoolBlue_Spider and run "scrapy crawl coolblue -o name_output_file.csv" to run the spider

I used Python 3.7.0 to get results. There is a requirements.txt available that also displays everything I'm using. Besides the default pip and setuptools library, I installed scrapy and pywin32. Everything else came with that.

The folder CSV Files has 2 csv files that I got from running the spider in two different days (26 and  27 March)


CODE BREAKDOWN

The python code only requires two imports, scrapy and a custom item I created at "items.py" to hold up a product's information (Url, price, promotional price).

As required by the scrapy framework, i declare the class. The url I am using as a starting point is "https://www.coolblue.nl/en/our-assortment"

I navigate pages by using xpath. The "declare_xpath" method gets all the references I needed to scrape the website. Tried to make the names as intuitive as possible, and added comments when I though it was necessary.

There are 2 parser functions. The first, "parse", is meant to gather all the URL's to product pages. It can gather this information from 3 possible kind of sources:

- The assortment page
- A page with a grid and an index of subcategories
- A page with a list of products, which also has a, index of subcategories

The second, "parse_product", scrapes the product pages and gathers the url, the price and the promotional price.
