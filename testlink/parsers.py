#!/usr/bin/env python

"""
@author: Kai Borowiak
@summary: Common parsers for Testlink internals
"""

# IMPORTS
import HTMLParser
from bs4 import BeautifulSoup
from .log import tl_log as log


class DefaultParser(HTMLParser.HTMLParser):
	"""Default parser, just unescape fed data"""

	def __init___(self):
		HTMLParser.HTMLParser(self)

	def feed(self,data):
		return HTMLParser.HTMLParser.unescape(self,data)


class ListParser(object):
	"""Parses (un)numbered lists to python lists"""

	def feed(self,data):
		soup = BeautifulSoup(data)
		if soup.ul:
			return self.listify(soup.ul)
		elif soup.ol:
			return self.listify(soup.ol)
		else:
			return data

	def listify(self,html):
		result = []
		for li in html.find_all('li',recursive=False):
			try:
				elem = next(li.stripped_strings)
				result.append( elem )
				if li.find('ul'):
					result.append( self.listify(li.find('ul')) )
				elif li.find('ol'):
					result.append( self.listify(li.find('ol')) )
			except StopIteration:
				break
		return result