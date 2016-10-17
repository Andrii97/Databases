from lxml import html
from lxml import etree
import requests


def load_page(url):
	page = requests.get(url)
	tree_ = html.fromstring(page.content)
	return tree_

if __name__ == '__main__':
	root = etree.Element('data')
	doc = etree.ElementTree(root)
	page_element = etree.SubElement(root, 'page', url="http://freedelivery.com.ua/arduino-100/akssesuary-129/")

	tree = load_page('http://freedelivery.com.ua/arduino-100/akssesuary-129/')

	images = tree.xpath('//img[@class="img-responsive center-block"]/@src')
	prices = tree.xpath('//p[@class="price"]/text()')
	descriptions = tree.xpath('//p[@class="description"]/text()')

	for i in range(0, 21):
		product_element = etree.SubElement(root, 'product')
		name_element = etree.SubElement(product_element, 'price')
		name_element.text = prices[i]
		desc_element = etree.SubElement(product_element, 'description')
		desc_element.text = descriptions[i]
		image_element = etree.SubElement(product_element, 'image')
		image_element.text = images[i]
	doc.write('task3.xml', xml_declaration=True, encoding='utf-16')


