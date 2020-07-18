<?xml version="1.0" encoding="iso-8859-1"?>
<xsl:stylesheet
    version="2.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:tlm="http://www.thinkulum.net/"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    >
    <xsl:output method="text"/>

    <xsl:variable name="tab" select="'&#x09;'"/>
    <xsl:variable name="newline" select="'&#x0a;'"/>

    <xsl:template match="/">
        <xsl:apply-templates/>

        <xsl:apply-templates select="//li[ @key ][ not(li) ]"/>
    </xsl:template>

    <xsl:template match="notes|li[ @key or li ]">
        <xsl:variable name="self" select="."/>
        <xsl:variable name="breadcrumb">
            <xsl:for-each select="ancestor-or-self::*">
                <xsl:sort select="position()" order="ascending"/>
                <xsl:if test="name(.) = 'li' or $self is /notes">
                    <xsl:value-of select="tlm:elt_string(.)"/>
                    <xsl:if test="position() != last()">
                        <xsl:text> &gt; </xsl:text>
                    </xsl:if>
                </xsl:if>
            </xsl:for-each>
        </xsl:variable>

        <xsl:call-template name="add_list_flashcard">
            <xsl:with-param name="elt" select="$self"/>
            <xsl:with-param name="breadcrumb" select="$breadcrumb"/>
        </xsl:call-template>

        <xsl:apply-templates select="li[ li ]"/>
    </xsl:template>

    <xsl:template match="li[ not(@key) ][ not(li) ]"/>

    <xsl:function name="tlm:elt_string">
        <xsl:param name="elt"/>

        <xsl:choose>
            <xsl:when test="$elt instance of xs:string">
                <xsl:value-of select="$elt"/>
            </xsl:when>
            <xsl:when test="$elt instance of xs:integer">
                <xsl:value-of select="string($elt)"/>
            </xsl:when>
            <xsl:when test="name($elt) = 'notes'">
                <xsl:value-of select="name($elt)"/>
            </xsl:when>
            <xsl:when test="not(empty($elt[@key]))">
                <!-- <xsl:text>{key} </xsl:text> --><xsl:value-of select="$elt/@key"/>
            </xsl:when>
            <xsl:when test="count($elt/li) = 0">
                <!-- <xsl:text>{no children} </xsl:text> --><xsl:value-of select="$elt"/>
            </xsl:when>
        </xsl:choose>
    </xsl:function>

    <xsl:template name="add_list_flashcard">
        <xsl:param name="elt"/>
        <xsl:param name="breadcrumb"/>

        <xsl:text>---</xsl:text>
        <xsl:value-of select="$newline"/>

        <xsl:value-of select="$breadcrumb"/>
        <xsl:value-of select="$newline"/>
        <xsl:value-of select="$newline"/>

        <xsl:choose>
            <xsl:when test="$elt/li">
                <xsl:value-of select="count($elt/li)"/>
                <xsl:value-of select="$newline"/>

                <xsl:for-each select="$elt/li">
                    <xsl:value-of select="tlm:elt_string(.)"/>
                    <xsl:value-of select="$newline"/>
                </xsl:for-each>
            </xsl:when>

            <xsl:otherwise>
                <xsl:value-of select="$elt"/>
                <xsl:value-of select="$newline"/>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

</xsl:stylesheet>