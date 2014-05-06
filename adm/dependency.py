import os

class Dependency:
	'Model for containing data about a dependency'

	def __init__(self, name, url):
		self.name = name
		self.url = url
		self.branch = "master"
		self.tag = None
		self.commit = None