import collections
import logging
import csv

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('wb')

ParseResult = collections.namedtuple(
    'ParseResult',
    (
        'product_brand',
        'product_name',
        'product_price',
        'product_link',
        'product_img',
        'product_sizes'
    )
)

HEADERS = (
    'product_brand',
    'product_name',
    'product_price',
    'product_link',
    'product_img',
    'product_sizes'
)


class Client:

    def __init__(self):
        self.result = []
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()

    def load_page(self, url, driver):
        print(url, type(url))
        driver.get(url)

    def parse_page(self):
        products = self.driver.find_elements_by_class_name("productThumbnailItem")
        if not products:
            logger.error('No such block PRODUCTS')
        else:
            #for product in products:
            for i in range(2):
                self.parse_block(block=products[i])
            print(self.result)
        self.driver.close()

    def save_results(self):
        path = '/Users/KRASAVA/PycharmProjects/selenium/result.csv'
        with open(path, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(HEADERS)
            for item in self.result:
                writer.writerow(item)

    def parse_block(self, block):
        try:
            brand = block.find_element_by_class_name('productBrand').text
            name = block.find_element_by_class_name('productDescLink').get_attribute("title")
            price = block.find_element_by_class_name('priceInfo').text
            link = block.find_element_by_class_name('productDescLink').get_attribute("href")
            img = block.find_element_by_class_name('thumbnailImage').get_attribute("src")
        except NoSuchElementException:
            logger.error('No such block')
            return

        sizes = self.parse_inner_page(link)

        self.result.append(ParseResult(
            product_brand=brand,
            product_name=name,
            product_price=price,
            product_link=link,
            product_img=img,
            product_sizes=sizes
        ))

    def parse_inner_page(self, link):
        inner_driver = webdriver.Chrome()
        self.load_page(str(link), inner_driver)
        sizes = inner_driver.find_elements_by_class_name('swatch-itm')
        list_sizes = []
        if not sizes:
            logger.error('No such block SIZES')
        else:
            for size in sizes:
                size_not_active = size.get_attribute("aria-disabled")
                size_name = size.text
                print(size_name, size)
                saze_data = {'size_not_active': size_not_active, 'size_name': size_name}
                list_sizes.append(saze_data)
        inner_driver.close()
        return list_sizes

    def run(self):
        url = 'https://www.macys.com/shop/shoes/all-womens-shoes?id=56233&cm_sp=intl_hdr-_-women-_-56233_all-women' \
              '%27s-shoes_COL2 '
        self.load_page(url, self.driver)
        self.parse_page()
        logging.info(f'You get {len(self.result)} items')
        self.save_results()


if __name__ == '__main__':
    parser = Client()
    parser.run()
