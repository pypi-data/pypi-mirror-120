<?xml version="1.0" encoding="UTF-8"?>
<!-- 
    
    XSL Stylesheet for Feed format transformation
        ATOM : https://validator.w3.org/feed/docs/atom.html
    to
        RSS 2 : https://validator.w3.org/feed/docs/rss2.html
                http://www.rssboard.org/rss-specification
        
    Released under CC BY-SA 3.0 FR https://creativecommons.org/licenses/by-sa/3.0/fr/
    author : Frederic Laurent
    
    Assumptions:
     - Atom feed is valid without warning
     - RSS2 feed will be valid without warning
     - Atom feed is named feedname.xml
     - RSS2 feed will be named feedname.rss2 (only the extension is changed)
-->

<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:atom="http://www.w3.org/2005/Atom"
    xmlns:pyext="http://www.opikanoba.org/ns/etree-extensions"
    exclude-result-prefixes="pyext"
    extension-element-prefixes="pyext"
    version="1.0">

    <xsl:import href="file://atom1_to_rss2.xsl"/>

    <!-- 
        Convert ISO date into RFC 822 format
        IN  : 2017-11-03T16:55:03.198512+00:00 
        OUT : SAT, 11 Nov 2017 16:55:03 +0000
    -->

    <xsl:template match="atom:updated">
        <pyext:formatdt></pyext:formatdt>
    </xsl:template>
    

</xsl:stylesheet>
