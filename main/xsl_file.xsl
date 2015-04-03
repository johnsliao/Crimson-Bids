<?xml version= "1.0"?>
<xsl:stylesheet version= "1.0"
xmlns:xsl= "http://www.w3.org/1999/XSL/Transform">

<xsl:template match="/">
  <html>
  <body>
  <h2>Item</h2>
  <table border="1">
    <tr bgcolor="#9acd32">
		<th>title</th>
		<th>itemId</th>
		<th>viewItemURL</th>
    <th>sellerUserName</th>
    <th>positiveFeedbackPercent</th>
    <th>feedbackRatingStar</th>
    <th>conditionId</th>
    <th>listingType</th>
    <th>currentPrice</th>
    <th>bidCount</th>
    <th>timeleft (days,hours,mins,sec)</th>
    </tr>
	<xsl:for-each select="root/item">
    <tr>
      <td><xsl:value-of select="title"/></td>
      <td><xsl:value-of select="itemId"/></td>
      <td><xsl:value-of select="viewItemURL"/></td>
      <td><xsl:value-of select="sellerUserName"/></td>
      <td><xsl:value-of select="positiveFeedbackPercent"/></td>
      <td><xsl:value-of select="feedbackRatingStar"/></td>
      <td><xsl:value-of select="conditionId"/></td>
      <td><xsl:value-of select="listingType"/></td>
      <td><xsl:value-of select="currentPrice"/></td>
      <td><xsl:value-of select="bidCount"/></td>
      <td><xsl:value-of select="timeLeft"/></td>
    </tr>
	</xsl:for-each>
  </table>
  </body>
  </html>
</xsl:template>

</xsl:stylesheet>