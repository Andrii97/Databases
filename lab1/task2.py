import lxml.etree as etree
tree = etree.parse("task1.xml")
count = tree.xpath("count(//image)")
i = tree.xpath("count(//page)")
print count / i, " cnt = ", count, " pages = ", i