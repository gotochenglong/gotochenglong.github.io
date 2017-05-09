#!/usr/bin/env python
# -*- coding:utf8 -*-
# Author: Wang Chenglong
# E-mail: gotochenglong@gmail.com
# Date: 2017-05-09 19:12:23
#coding=utf-8
import re
import urllib
import json

def getHtml(url):
    page = urllib.urlopen(url)
    html = page.read()
    return html.decode('utf-8')

def getPage(html):
    reg = u'随笔 - ([0-9]+)'
    pageCount = re.findall(reg,html)
    return pageCount[0]

def getArticleUrl(html):
    reg = r'(http://www.cnblogs.com/qiusuo/p/[0-9]+.html)'
    articleUrl = re.findall(reg,html)
    return articleUrl

def getTag(url):
    reg = r'/p/(\d+)\.html'
    postId = re.findall(reg, url)[0]
    tagurl = r'http://www.cnblogs.com/mvc/blog/CategoriesTags.aspx?blogApp=qiusuo&blogId=194853&postId=%s' % postId
    content = getHtml(tagurl)
    content = json.loads(content)['Tags']
    tagreg = r'\">(.*?)</a>'
    tags = re.findall(tagreg, content)
    return tags[0]
    
def saveTo(filename, content):
    writer = open(filename, "w")
    writer.write(content)
    writer.close()

def downloadPage(urlList):
    # x = 0
    for article in urlList:
        # x+=1
        # urllib.urlretrieve(article,'%s.html' % x)
        tag = getTag(article)
        content = getHtml(article)
        regtitle = r'<a id="cb_post_title_url" href=".*?">(.*?)</a>'
        regbody = r'<div id="cnblogs_post_body">([\s\S]*?)</div><div id="MySignature">'
        regdate = r'<span id="post-date">([\d\- :]+?)</span>'
        #print content

        title = re.findall(regtitle, content)[0]
        body = re.findall(regbody, content)[0]
        date = re.findall(regdate, content)[0]
        
        ## 转义liquid标签
        body = re.sub(r"(\{%.*?%\})", r"{% raw %}\1{% endraw %}", body)
        body = re.sub(r"(\{\{.*?\}\})", r"{% raw %}\1{% endraw %}", body)

        #print body
        print title
        print date
        print article
        print tag
        head = """---
layout: post
title:  "%s"
date:   %s +0800
categories: %s
tag:    %s
from:   %s
---
%s
""" % (title, date, tag.replace(" ", "_"), tag.replace(" ", "_"), article, body)
        filename = "/home/pi/project/gotochenglong.github.io/_posts/%s-%s.md" % (date[0:10], title.replace(" ", "-"))
        saveTo(filename, head.encode('utf-8'))
        #print head
        #exit(0)


article = []
htmlStr = getHtml("http://www.cnblogs.com/qiusuo/default.html")
pageCount = getPage(htmlStr)
page = int(pageCount)/10+1
for i in range(1,page+1):
    html = getHtml("http://www.cnblogs.com/qiusuo/default.html?page="+str(i))
    articleUrl = getArticleUrl(html)
    article = article.__add__(articleUrl)

article = list(set(article))
downloadPage(article)
