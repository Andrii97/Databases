<?xml version="1.0" encoding="UTF-16"?>
<xsl:transform version="1.0"
xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<!--<?xml-stylesheet type="text/xsl" href="task3.xsl"?>-->

<xsl:template match="/">
  <html>
      <head>
          <meta charset="utf-16"/>
      </head>
  <body>
  <h2>Одиссей</h2>
  <table border="1px solid blue">
    <tr>
      <th>Price</th>
      <th>Description</th>
      <th>Image</th>
    </tr>
    <xsl:for-each select="data/product">
    <tr>
      <td style="text-align:center"><xsl:value-of select="price"/></td>
      <td style="text-align:center"><xsl:value-of select="description"/></td>
      <td style="text-align:center">

	<img>
	    <xsl:attribute name="src">
		<xsl:value-of select="image"/>
	    </xsl:attribute>
	</img>
	</td>
    </tr>
    </xsl:for-each>
  </table>
  </body>
  </html>
</xsl:template>

</xsl:transform>