from lxml import html
from lxml import etree

import requests


def parse_html():
    root = etree.Element('data')
    print root
    doc = etree.ElementTree(root)
    print doc
    page = requests.get('http://www.ua.igotoworld.com/')
    tree = html.fromstring(page.content)
    link = tree.xpath('//a[not(@class)]/@href')

    counter, i = 0, 0

    while counter != 20:
        if "javascript" in link[i]:
            i += 1
            continue
        page = requests.get(link[i])
        tree = html.fromstring(page.content)
        images = tree.xpath('//img/@src')
        text = tree.xpath('//*[text()]')

        if text and images:
            print link[i]
            page_element = etree.SubElement(root, 'page',
                                            url=link[i])
            for t in text:
                if t.tag != "script" and t.text and not only_whitespaces(t.text):
                    text_fragment = etree.SubElement(page_element, 'text')
                    text_fragment.text = t.text
                    print t.text.encode('utf-8')
            for image in images:
                image_fragment = etree.SubElement(page_element, "image")
                image_fragment.text = image
            # print images
            counter += 1
        i += 1

    doc.write('task1.xml', xml_declaration=True, encoding='utf-16')

def only_whitespaces(str):
    for symbol in str:
        if symbol is not " ":
            continue
        else:
            return 1
    return 0


parse_html()