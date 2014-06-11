import os

class Dependency:
	'Model for containing data about a dependency'

	def __init__(self, name, url):
		self.name = name
		self.url = url
		self.branch = "master"
		self.tag = None
		self.commit = None
		self.extended_name = name
		self.path = None

	def __repr__(self):
		return '{ name: %s, url: %s, extended_name: %s }' % (self.name, self.url, self.extended_name)