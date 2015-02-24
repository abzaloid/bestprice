#-*- coding: utf-8  -*-

import urllib
import urllib2



p = urllib2.urlopen("http://arbuz.kz/ru/almaty/catalog/cat/19340-kapusta")
html = p.read()

from bs4 import BeautifulSoup

soup = BeautifulSoup(html)
#print (soup.prettify().encode('UTF-8'))


print u"кетсукар"