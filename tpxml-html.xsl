<?xml version="1.0" encoding="ISO-8859-1"?>

<xsl:stylesheet version="1.0"
xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:output method="html" indent="yes"/>

<xsl:template match="/project">
  <xsl:element name="html">
    <xsl:element name="head">
      <xsl:element name="link">
        <xsl:attribute name="rel">stylesheet</xsl:attribute>
        <xsl:attribute name="type">text/css</xsl:attribute>
        <xsl:attribute name="href">taskpaper.css</xsl:attribute>
      </xsl:element>
    </xsl:element>
    <xsl:element name="body">
      <xsl:element name="ul">
        <xsl:apply-templates />
      </xsl:element>
    </xsl:element>
  </xsl:element>
</xsl:template>

<xsl:template match="project">
  <xsl:element name="li"> 
    <xsl:attribute name="class">project</xsl:attribute>
    <xsl:value-of select="@name" />
    <xsl:text>:</xsl:text>
    <xsl:apply-templates select="tag" />
    <xsl:element name="ul">
      <xsl:attribute name="class">project</xsl:attribute>
      <xsl:apply-templates select="project|task|notes" />
    </xsl:element>
  </xsl:element>
</xsl:template>

<xsl:template match="task">
  <xsl:element name="li">
    <xsl:attribute name="class">task</xsl:attribute>
    <xsl:text>- </xsl:text>
    <xsl:value-of select="@name" />
    <xsl:apply-templates select="tag" />
    <xsl:element name="ul">
      <xsl:attribute name="class">task</xsl:attribute>
      <xsl:apply-templates select="project|task|notes" />
    </xsl:element>
  </xsl:element>
</xsl:template>

<xsl:template match="tag">
  <xsl:element name="span">
    <xsl:attribute name="class">tag tag-<xsl:value-of select="translate(., ' ', '_')" /></xsl:attribute>
    <xsl:text> @</xsl:text>
    <xsl:value-of select="." />
  </xsl:element>
</xsl:template>

<xsl:template match="notes">
  <xsl:element name="div">
    <xsl:attribute name="class">notes</xsl:attribute>
    <xsl:value-of select="." disable-output-escaping="yes"/>
  </xsl:element>
</xsl:template>

</xsl:stylesheet>
