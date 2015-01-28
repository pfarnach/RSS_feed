# Written by Pat Farnach
# NPR RSS Feed retriever, displays headlines

import urllib2, jinja2
import xml.etree.ElementTree as ET

class NPR_feed(object):

	def __init__(self, feed_ID):
		# retrieves and reads XML file then puts it into XML format for given RSS ID
		self._xml_response = urllib2.urlopen('http://www.npr.org/rss/rss.php?id=%s' % feed_ID).read()
		self._xml_root = ET.fromstring(self._xml_response)
		# self._xml_root[0][0].text


	def parse_xml(self):

		self._results = []

		# from channel tag, look for immediate 'item' children and put their children into dictionary
		for index, item in enumerate(self._xml_root[0].findall('item')):
			self._results.append([])
			self._results[index] = {}
			self._results[index]['title'] = item[0].text # title
			self._results[index]['description'] = item[1].text # description
			self._results[index]['pub_date'] = item[2].text[:-6] # pub date, cuts off microseconds
			self._results[index]['link'] = item[3].text # link 

			# try to get the author but may not exist
			try:
				self._results[index]['author'] = item[6].text # author
			except IndexError:
				self._results[index]['author'] = 'None' # author


	def display(self):

		# loops through list and prints out dictionaries inside it containing parsed XML info
		for item in self._results:
			print
			print item['title']
			print
			print item['description']
			print
			print item['pub_date']
			print
			print item['link']
			print
			print item['author']
			print
			print '*'*10


	def pass_to_template(self):

		parsed_list = self._results

		# Using a template file. Load template files from the current directory
		env = jinja2.Environment(loader=jinja2.FileSystemLoader('.'))
		tp = env.get_template('RSS_feed.html')
		output_list = tp.render(parsed_list = parsed_list, feed_title = self._xml_root[0][0].text)

		with open('test.html', 'wb') as output:
			output.write(output_list)


def main():
	print "\nSome popular IDs include:\n1001 - News Headlines\n1008 - Arts & Culture\n1057 - Opinion\n1003 - US News\n1004 - World News\n2 - All Things Considered\n37 - All Songs Considered"
	feed_ID = raw_input("\n>>Please enter an NPR Feed ID: ").strip()
	feed = NPR_feed(feed_ID)
	feed.parse_xml()
	# feed.display()
	feed.pass_to_template()


if __name__ == "__main__":
	main()