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
    xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:atom="http://www.w3.org/2005/Atom"
    exclude-result-prefixes="xs" version="2.0">

    <!-- 
       main element : feed container  
    -->
    <xsl:template match="/atom:feed">
        <rss version="2.0">
            <channel>
                <!-- Required elements : title, link, description -->
                <!-- Optionnal elements : language, copyright, managingEditor,webMaster,pubDate,
                laastBuildDate,category,generator,docs,cloud,ttl,image,rating,textInput,skipHours,skipDays  -->
                <xsl:comment>Atom feed ID = <xsl:value-of select="atom:id/text()"/></xsl:comment>
                <title>
                    <xsl:choose>
                        <xsl:when test="atom:title">
                            <xsl:apply-templates select="atom:title"/>
                        </xsl:when>
                        <xsl:otherwise>#BAD : Atom title not defined</xsl:otherwise>
                    </xsl:choose>
                </title>
                <!-- Change the extension of the RSS2 feed name -->
                <atom:link
                    href="{concat(substring-before(atom:link[@rel='self']/@href,'.xml'),'.rss2')}"
                    rel="self" type="application/rss+xml"/>
                <link>
                    <xsl:choose>
                        <xsl:when test="atom:link[@rel = 'related']">
                            <xsl:apply-templates select="atom:link[@rel = 'related']/@href"/>
                        </xsl:when>
                        <xsl:when test="not(atom:link[@rel = 'related']) and atom:link">
                            <xsl:apply-templates select="atom:link[1]/@href"/>
                        </xsl:when>
                        <xsl:otherwise>#BAD : Atom link, type related, not defined</xsl:otherwise>
                    </xsl:choose>
                </link>
                <description>
                    <xsl:choose>
                        <xsl:when test="atom:subtitle">
                            <xsl:apply-templates select="atom:subtitle"/>
                        </xsl:when>
                        <xsl:otherwise>#BAD : Atom subtitle not defined</xsl:otherwise>
                    </xsl:choose>
                </description>
                <xsl:if test="atom:rights">
                    <copyright>
                        <xsl:apply-templates select="atom:rights"/>
                    </copyright>
                </xsl:if>
                <xsl:if test="atom:author/atom:email">
                    <managingEditor>
                        <xsl:apply-templates select="atom:author" mode="email"/>
                    </managingEditor>
                </xsl:if>
                <pubDate><xsl:apply-templates select="atom:updated"/></pubDate>
                <lastBuildDate><xsl:apply-templates select="atom:updated"/></lastBuildDate>
                <xsl:if test="@xml:lang">
                    <language>
                        <xsl:value-of select="@xml:lang"/>
                    </language>
                </xsl:if>
                <xsl:apply-templates select="atom:category"/>

                <generator>XSL stylesheet - http://github.com/flrt/xsl_atom2rss2</generator>
                <xsl:if test="atom:generator">
                    <xsl:comment>Atom feed generator : <xsl:value-of select="atom:generator/@uri"/> </xsl:comment>
                </xsl:if>
                <xsl:if test="atom:link[@rel = 'related']">
                    <docs>
                        <xsl:value-of select="atom:link[@rel = 'related']/@href"/>
                    </docs>
                </xsl:if>
                <!-- SKIP TAG : cloud -->
                <!-- SKIP TAG : ttl -->
                <xsl:if test="atom:logo">
                    <image>
                        <url>
                            <xsl:value-of select="atom:logo/text()"/>
                        </url>
                    </image>
                </xsl:if>
                <!-- SKIP TAG : textInput -->
                <!-- SKIP TAG : skipHours -->
                <!-- SKIP TAG : skipDays -->

                <xsl:apply-templates select="atom:entry"/>
            </channel>
        </rss>
    </xsl:template>

    <xsl:template match="atom:category">
        <category>
            <xsl:if test="@scheme">
                <xsl:attribute name="domain">
                    <xsl:value-of select="@scheme"/>
                </xsl:attribute>
            </xsl:if>
            <xsl:value-of select="@term"/>
            <xsl:if test="@label and not(@label = @term)">
                <xsl:comment>Atom category label : <xsl:value-of select="@label"/></xsl:comment>
            </xsl:if>
        </category>
    </xsl:template>

    <!-- 
        Element entry becomes item
        
    -->

    <xsl:template match="atom:entry">
        <item>
            <title>
                <xsl:value-of select="atom:title/text()"/>
            </title>
            <xsl:if test="atom:link[@rel = 'alternate']">
                <link>
                    <xsl:value-of select="atom:link[@rel = 'alternate']/@href"/>
                </link>
            </xsl:if>
            <xsl:if test="atom:content">
                <description>
                    <xsl:choose>
                        <!-- content already escaped -->
                        <xsl:when test="atom:content[@type = 'text' or @type = 'html']">
                            <xsl:value-of select="atom:content/text()"/>
                        </xsl:when>
                        <!-- content XML, need to be escaped -->
                        <xsl:when test="atom:content[@type = 'xhtml']">
                            <xsl:apply-templates select="atom:content/*" mode="escapeXML"/>
                        </xsl:when>
                    </xsl:choose>

                </description>
            </xsl:if>
            <xsl:if test="atom:author">
                <!-- author/name is required -->
                <author>
                    <xsl:apply-templates select="atom:author" mode="email"/>
                </author>
            </xsl:if>
            <xsl:apply-templates select="atom:category"/>
            <!-- SKIP : comments -->
            <!-- SKIP : enclosure -->

            <guid>
                <xsl:value-of select="atom:id/text()"/>
            </guid>
            <pubDate><xsl:apply-templates select="atom:updated"/></pubDate>
            <xsl:choose>
                <xsl:when test="atom:source/atom:id and atom:source/atom:title">
                    <source url="{atom:source/atom:id/text()}">
                        <xsl:value-of select="atom:source/atom:title"/>
                    </source>
                </xsl:when>
                <xsl:when test="not(atom:source/atom:id) and atom:source/atom:title">
                    <source>
                        <xsl:value-of select="atom:source/atom:title/text()"/>
                    </source>
                </xsl:when>
            </xsl:choose>
        </item>
    </xsl:template>


    <!-- 
        Copy XHTML tree with tags, atrr, and ns
    -->
    <xsl:template match="@* | node()" mode="xhtml">
        <xsl:copy>
            <xsl:apply-templates select="@* | node()" mode="xhtml"/>
        </xsl:copy>
    </xsl:template>

    <!-- 
        Produce the email value : me@mail.com (ME) or ME if email doesn't exist
    -->
    <xsl:template match="atom:author" mode="email">
        <xsl:choose>
            <xsl:when test="atom:email and atom:name">
                <xsl:value-of select="concat(atom:email/text(), ' (', atom:name/text(), ')')"/>
            </xsl:when>
            <xsl:otherwise>
                <xsl:value-of select="atom:name/text()"/>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

    <!-- 
        Convert ISO date into RFC 822 format
        IN  : 2017-11-03T16:55:03.198512+00:00 
        OUT : SAT, 11 Nov 2017 16:55:03 +0000
    -->

    <xsl:template match="atom:updated">
        <xsl:value-of
            select="format-dateTime(xs:dateTime(.), '[FNn,*-3], [D00] [MNn,*-3] [Y] [H00]:[m00]:[s00] [Z0000]', 'en', (), ())"/>
    </xsl:template>
    
    <!-- 
        Escape XML elements by replacing <, >, " by HTML entities
        
    -->

    <xsl:template match="*" mode="escapeXML">
        <xsl:value-of select="concat('&lt;', name())"/>
        <xsl:for-each select="@*">
            <xsl:value-of select="concat(' ', name(), '=&quot;', ., '&quot;')"/>
        </xsl:for-each>
        <xsl:value-of select="'&gt;'"/>
        <xsl:apply-templates mode="escapeXML"/>
        <xsl:value-of select="concat('&lt;/', name(), '&gt;')"/>
    </xsl:template>

</xsl:stylesheet>
