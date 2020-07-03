<?xml version="1.0" encoding="iso-8859-1"?>
<xsl:stylesheet
    version="2.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:tlm="http://www.thinkulum.net/"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    >
<xsl:output method="text"/>

<!-- <xsl:variable name="tab" select="'&#x09;'"/> -->
<xsl:variable name="tab" select="': '"/>
<xsl:variable name="newline" select="'&#x0a;'"/>

<xsl:template match="/">
    <xsl:apply-templates/>
</xsl:template>

<xsl:template match="outline|li">
    <xsl:variable name="self" select="."/>
    <xsl:variable name="breadcrumb">
        <xsl:for-each select="ancestor-or-self::*">
            <xsl:sort select="position()" order="ascending"/>
            <xsl:if test="name(.) = 'li' or $self is /outline">
                <xsl:value-of select="tlm:elt_string(.)"/>
                <xsl:if test="position() != last()">
                    <xsl:text> &gt; </xsl:text>
                </xsl:if>
            </xsl:if>
        </xsl:for-each>
    </xsl:variable>
    <!-- parent -->
<!--
    <xsl:call-template name="add_flashcard">
        <xsl:with-param name="elt" select="$self"/>
        <xsl:with-param name="target" select=".."/>
        <xsl:with-param name="axis" select="'parent'"/>
        <xsl:with-param name="breadcrumb" select="$breadcrumb"/>
    </xsl:call-template>
-->
    <!-- value -->
    <xsl:call-template name="add_flashcard">
        <xsl:with-param name="elt" select="$self"/>
        <xsl:with-param name="target" select="./text()"/>
        <xsl:with-param name="axis" select="'value'"/>
        <xsl:with-param name="breadcrumb" select="$breadcrumb"/>
    </xsl:call-template>
    <!-- child count -->
    <xsl:call-template name="add_flashcard">
        <xsl:with-param name="elt" select="$self"/>
        <xsl:with-param name="target" select="count(*)"/>
        <xsl:with-param name="axis" select="'child count'"/>
        <xsl:with-param name="breadcrumb" select="$breadcrumb"/>
    </xsl:call-template>
    <!-- first child -->
    <xsl:call-template name="add_flashcard">
        <xsl:with-param name="elt" select="$self"/>
        <xsl:with-param name="target" select="*[1]"/>
        <xsl:with-param name="axis" select="'first child'"/>
        <xsl:with-param name="breadcrumb" select="$breadcrumb"/>
    </xsl:call-template>
    <!-- previous sibling -->
<!--
    <xsl:call-template name="add_flashcard">
        <xsl:with-param name="elt" select="$self"/>
        <xsl:with-param name="target" select="preceding-sibling::*[1]"/>
        <xsl:with-param name="axis" select="'previous sibling'"/>
        <xsl:with-param name="breadcrumb" select="$breadcrumb"/>
    </xsl:call-template>
-->
    <!-- next sibling -->
    <xsl:call-template name="add_flashcard">
        <xsl:with-param name="elt" select="$self"/>
        <xsl:with-param name="target" select="following-sibling::*[1]"/>
        <xsl:with-param name="axis" select="'next sibling'"/>
        <xsl:with-param name="breadcrumb" select="$breadcrumb"/>
    </xsl:call-template>
    <!-- next element -->
    <!-- <xsl:call-template name="add_flashcard">
        <xsl:with-param name="elt" select="$self"/>
        <xsl:with-param name="target" select="if (descendant::*[1]) 
                                              then descendant::*[1] 
                                              else following::*[1]"/>
        <xsl:with-param name="axis" select="'next element'"/>
        <xsl:with-param name="breadcrumb" select="$breadcrumb"/>
    </xsl:call-template> -->

    <xsl:apply-templates select="li"/>
</xsl:template>

<xsl:function name="tlm:elt_string">
    <xsl:param name="elt"/>

    <xsl:text>'</xsl:text>
    <xsl:choose>
        <xsl:when test="$elt instance of xs:string">
            <xsl:value-of select="$elt"/>
        </xsl:when>
        <xsl:when test="$elt instance of xs:integer">
            <xsl:value-of select="string($elt)"/>
        </xsl:when>
        <xsl:when test="name($elt) = 'outline'">
            <xsl:value-of select="name($elt)"/>
        </xsl:when>
        <xsl:when test="not(empty($elt[@key]))">
            <!-- <xsl:text>{key} </xsl:text> --><xsl:value-of select="$elt/@key"/>
        </xsl:when>
        <xsl:when test="count($elt/li) = 0">
            <!-- <xsl:text>{no children} </xsl:text> --><xsl:value-of select="$elt"/>
        </xsl:when>
    </xsl:choose>
    <xsl:text>'</xsl:text>
</xsl:function>

<xsl:template name="add_flashcard">
    <xsl:param name="elt"/>
    <xsl:param name="target"/>
    <xsl:param name="axis"/>
    <xsl:param name="breadcrumb"/>

    <xsl:if test="not(empty($target)) 
                  and not( $target instance of node() and $target is / )
                  and not( $axis = 'value' and empty($elt[@key]) )">
        <xsl:choose>
            <xsl:when test="$axis = 'parent'">
                <xsl:value-of select="tlm:elt_string($elt)"/>
            </xsl:when>
            <xsl:otherwise>
                <xsl:value-of select="$breadcrumb"/>
            </xsl:otherwise>
        </xsl:choose>
        <xsl:text> </xsl:text>
        <xsl:value-of select="$axis"/>
        <xsl:value-of select="$tab"/>
        <xsl:value-of select="tlm:elt_string($target)"/>
        <xsl:value-of select="$newline"/>
    </xsl:if>
</xsl:template>

</xsl:stylesheet>