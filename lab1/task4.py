import lxml.etree as etree


data = open('task3.xsl')
xslt_content = data.read()
xslt_root = etree.XML(xslt_content)
dom = etree.parse('task3.xml')
transform = etree.XSLT(xslt_root)
result = transform(dom)
f = open('task4.html', 'w')
f.write(str(result))
f.close()