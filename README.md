# Web Scraping

*The readme is still under renovation. Please be patient as I am quite busy (lazy) at the moment. Merci beaucoup!*

<br>

## Intro

My understanding of web scraping is patience and attention to details. Scraping is not rocket science (deep learning is). When I do scraping, I typically spend 50% of my time in analyzing the source (navigate through HTML parse tree or inspect element to find the post form) and the rest 50% in ETL. The process does not require much brain power but it is quite time-consuming. Again, patience and attention to details matter. 

This repository contains a couple of python web scrapers. These scrapers mainly target at different commodity future exchanges and influential media websites (or so-called fake news, lol). Most scripts were written during my early days of Python learning. Since this repository gained unexpected popularity, I have restructured everything to make it more user-friendly. All the scripts featured in this repository are ready for use. Each script is designed to feature a unique technique that I found useful throughout my experience of data engineering. 

Scripts inside this repository are classified into two groups, beginner and advanced. At the beginning, the script is merely about some technique to extract the data. As you progress, the script leans more towards data architect and other functions to improve the end product. If you are experienced or simply come to get scrapers for free, you may want to skip the content and just look at <a href= https://github.com/je-suis-tm/web-scraping#available-scrapers>available scrapers</a>. If you are here to learn, you may look at <a href= https://github.com/je-suis-tm/web-scraping#table-of-contents>table of contents</a> to determine which suits you best. In addition, there are some <a href= https://github.com/je-suis-tm/web-scraping#notes>notes</a> on the annoying issues such as proxy authentication (usually corporate or university network) and legality (hopefully you won’t come to that).

<br>

## Table of Contents

#### Beginner

<a href=https://github.com/je-suis-tm/web-scraping#1-html-parse-tree-search-cme1>1. HTML Parse Tree Search (CME1)</a>

<a href=https://github.com/je-suis-tm/web-scraping#2-json-cme2>2. JSON (CME2)</a>

<a href=https://github.com/je-suis-tm/web-scraping#3-regular-expression-shfe>3. Regular Expression (SHFE)</a>

#### Advanced

<a href=https://github.com/je-suis-tm/web-scraping#1-sign-in-cqf>1. Sign-in (CQF)</a>

<a href=https://github.com/je-suis-tm/web-scraping#2-database-lme>2. Database (LME)</a>

<a href=https://github.com/je-suis-tm/web-scraping#3-newsfeed-mena>3. Newsfeed (MENA)</a>

#### Notes

<a href=https://github.com/je-suis-tm/web-scraping#1-proxy-authentication>1. Proxy Authentication</a>

<a href=https://github.com/je-suis-tm/web-scraping#2-ethics>2. Ethics</a>

<br>

## Available Scrapers

<a href=https://github.com/je-suis-tm/web-scraping/blob/master/MENA%20Newsfeed.py>1. Wall Street Journal WSJ</a>

<a href=https://github.com/je-suis-tm/web-scraping/blob/master/MENA%20Newsfeed.py>2. Financial Times FT</a>

<a href=https://github.com/je-suis-tm/web-scraping/blob/master/MENA%20Newsfeed.py>3. Bloomberg</a>

<a href=https://github.com/je-suis-tm/web-scraping/blob/master/MENA%20Newsfeed.py>4. Thompson Reuters</a>

<a href=https://github.com/je-suis-tm/web-scraping/blob/master/MENA%20Newsfeed.py>5. Al Jazeera AJ</a>

<a href=https://github.com/je-suis-tm/web-scraping/blob/master/MENA%20Newsfeed.py>6. British Broadcasting Corporation BBC</a>

<a href=https://github.com/je-suis-tm/web-scraping/blob/master/MENA%20Newsfeed.py>7. Fortune</a>

<a href=https://github.com/je-suis-tm/web-scraping/blob/master/MENA%20Newsfeed.py>8. Cable News Network CNN</a>

<a href=https://github.com/je-suis-tm/web-scraping/blob/master/MENA%20Newsfeed.py>9. The Economist</a>

<a href=https://github.com/je-suis-tm/web-scraping/blob/master/LME.py>10. London Metal Exchange LME</a>

<a href=https://github.com/je-suis-tm/web-scraping/blob/master/CME2.py>11. Chicago Merchantile Exchange CME</a>

<a href=https://github.com/je-suis-tm/web-scraping/blob/master/SHFE.py>12. Shanghai Future Exchange SHFE</a>

<a href=https://github.com/je-suis-tm/web-scraping/blob/master/CQF.py>13. Certificate in Quantitative Finance CQF</a>

<br>

## Beginner

#### 1. HTML Parse Tree Search (CME1)

Tree is an abstract data type in computer science. Now that you are a programmer, Binary Tree and AVL Tree must feel like primary school math (haha, I am joking, tree is my worst nightmare when it comes to interview). For a webpage, if you right click and select view source (CTRL+U in both IE & Chrome), you will end up with a bunch of codes like this.

![Alt Text](https://github.com/je-suis-tm/web-scraping/blob/master/preview/cme1%20html.PNG)

The codes are written in HTML. The whole HTML script is a tree structure as well. The HTML parse tree looks like this. 

![Alt Text](https://github.com/je-suis-tm/web-scraping/blob/master/preview/cme1%20tree.png)

There is something interesting about HTML parse tree. The first word after the left bracket is HTML tag (in tree structure we call it node). In most cases, tags come in pairs. Of course, there are some exceptions such as line break tag `<br>` or doc type tag ` <!DOCTYPE>`. Usually the opening tag is just tag name but the closing tag has a slash before the name. Different tag names represent different functionalities. In most cases, there are only a few tags that contain information we need, e.g., tag `<div>` usually defines a table, tag `<a>` creates a hyperlink (the link is at attribute `href` and it may skip prefix if the prefix is the same as current URL), tag `<img>` comes up with a pic (the link is hidden in attribute `src`), tag `<p>` or `<h1>`-`<h6>` normally contains text. For more details of tagging, please refer to <a href= https://www.w3schools.com/tags/default.asp>w3schools</a>.

It is vital to understand the basics of HTML parse tree because most websites with simple layout can easily be traversed via a library called BeautifulSoup. When we use urllib or other packages to request a specific website via python, we end up with HTML parse tree in bytes. When the bytes are parsed to BeautifulSoup, it makes life easier. It allows us to search the tag name and other attributes to get the content we need. The link to the documentation of BeautifulSoup is <a href= https://www.crummy.com/software/BeautifulSoup/bs4/doc>here</a>.

For instance, we would love to get the link to quiz on Dragon Ball, we can do

`result.find(‘div’,class_=’article article__list old__article-square’).find(‘a’).get(‘href’)`

Here, result is a BeautifulSoup object. The attribute `find` returns the first matched tag. The attribute `get` enables us to seek for attributes inside a tag.

Or we are interested in all the titles of the articles, we do

`temp=result.find(‘div’,class_=’article article__list old__article-square’).find_all(‘a’)` 

`output=[i.text for i in temp]`

The attribute `find_all` returns all the matched results. Note that the second article has a subtitle ‘subscriber only’, we will have a rather longer title for the second article. 

You can refer to <a href= https://github.com/je-suis-tm/web-scraping/blob/master/CME1.py>CME1</a> for more details. Please note that CME1 is an outdated script for Chicago Mercantile Exchange. Due to the change of the website, you cannot go through HTML parse tree to extract data any more. Yet, the concept of HTML parse tree is still applicable to other cases.

#### 2. JSON (CME2)

JSON, is the initial for JavaScript Object Notation. Like csv, it is another format to store data. According to the <a href=https://www.json.org>official website</a> of JSON, it is easy for humans to read and write. Pfff, are you fxxking kidding me? If you open JSON with notepad, you will see something like this.

![Alt Text](https://github.com/je-suis-tm/web-scraping/blob/master/preview/cme2%20json.PNG)

Gosh, the structure is messy and I will have a panic attack very soon. Just kidding. If you are familiar with adjacency list in graph theory, you will find it very easy to understand JSON. If not, do not worry, JSON is merely dictionaries inside dictionaries (with some lists as well). To navigate through the data structure, all you need to know is the key of the value.
Reading a JSON file in Python is straight forward. There are two ways.
There is a default package just called json, you can do

`import json`

`with open('data.json') as f:`

`	data = json.load(f)`

`print(data)`

Nevertheless, I propose a much easier way. We can parse the content to pandas and treat it like a dataframe. You can do

`import pandas as pd`

`df=pd.read_json('data.json')`

`print(df)`

Reading JSON is not really the main purpose of this chapter. What really made me rewrite the scraper for CME is the change of website structure. In April 2018, I could not extract data from searching for HTML tags any more. I came to realize that CME used JavaScript to create a dynamic website. The great era of BeautifulSoup was water under the bridge. At this critical point of either adapt or die, I had to find out where the data came from. Guess where?

![Alt Text](https://github.com/je-suis-tm/web-scraping/blob/master/preview/cme2%20url.PNG)

The URL is still in page source! The HTML tag for the hidden link is `<script>`. As I have mentioned at the beginning of this README file, scraping is about patience and attention to details. If you try to search all `<script>` tags, you will end up with more than 100 results. My friends, patience is a virtue. 
As for other websites, we may not be that lucky. Take <a href= https://www.euronext.com/en/products/indices/FR0003502079-XPAR>Euronext</a> for example, you won’t find any data in page source. We have to right click and select inspect element (CTRL+SHIFT+I in Chrome, F12 in IE).

![Alt Text](https://github.com/je-suis-tm/web-scraping/blob/master/preview/cme2%20inspect%20element.png)

The next step is to select Network Monitor in a pop-up window. Now let’s view data.

![Alt Text](https://github.com/je-suis-tm/web-scraping/blob/master/preview/cme2%20network.PNG)

There is a lot of traffic. Each one contains some information. Currently what truly matters to us is the request URL. Other information such as header or post form data will be featured in a later chapter. We must go through all the traffic to find out which URL leads to a JSON file. Once we hit the jackpot, we right click the request and copy link address.

![Alt Text](https://github.com/je-suis-tm/web-scraping/blob/master/preview/cme2%20request%20url.PNG)

![Alt Text](https://github.com/je-suis-tm/web-scraping/blob/master/preview/cme2%20link%20address.png)

Voila!

![Alt Text](https://github.com/je-suis-tm/web-scraping/blob/master/preview/cme2%20euronext.PNG)

You can refer to <a href= https://github.com/je-suis-tm/web-scraping/blob/master/CME2.py>CME2</a> for more details. Please note that CME2 is currently the available scraper for Chicago Mercantile Exchange.

#### 3. Regular Expression (SHFE)

<br>

## Advanced

#### 1. Sign-in (CQF)

#### 2. Database (LME)

#### 3. Newsfeed (MENA)

<br>

## Notes

#### 1. Proxy Authentication

#### 2. Ethics

