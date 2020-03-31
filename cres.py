import re
import csv
try:
	from StringIO import StringIO
except:
	from io import StringIO
from urllib2 import Request, urlopen, HTTPError
from urllib import urlencode, quote_plus
import xml.etree.ElementTree as ET

citation_output = "course_code;course_title;section;professor1;professor2;professor3;professor4;author;title;edition;isbn;book_code\n"

text = open('cres.txt','rb').read()
mytext = text.decode('utf-16')
mytext = mytext.encode('ascii','ignore')
newinput = open('bn_courses.txt','wb')
newinput.write(mytext)
newinput.close()

reader = open('newinput.txt','rb')

for line_of_text in reader:
	course_code_index = re.search('LAW\s7[0-9]{3}', line_of_text)
	isbn_index = re.search('[0-9]{13}', line_of_text)
	if course_code_index:
		reader2 = csv.DictReader(open('peoplesoft-courses.csv','r'))
		course_code = line_of_text[7:11].strip()
		section = line_of_text[29:32].strip()
		for row in reader2:
			if course_code == row['Catalog Nbr'] and section == row['Class Section']:
				course_title = row['Description']
				professors = row['Instructor (Role)']
				break
			else:
				continue
		#professors = line_of_text[74:97]
		professors = professors.replace(' (PI)','')
		professors = professors.replace(', ',';')
		professors = professors.rstrip(';')
		#print course_title, professors
		professor_count = professors.count(';') + 1
		if professor_count == 1:
			professors = professors + ";;;"
		elif professor_count == 2:
			professors = professors + ";;"
		elif professor_count == 3:
			professors = professors + ";"
		else:
			pass
	elif line_of_text.find('---------------------------------------------------------') != -1:
		continue
	elif line_of_text.find('No Text Required') != -1:
		continue
	elif isbn_index:
		author = line_of_text[4:19]
		author = author.strip()
		title = line_of_text[19:55]
		title = title.strip()
		edition = line_of_text[55:60]
		edition = edition.strip()
		isbn = line_of_text[93:108]
		isbn = isbn.strip()
		book_code = line_of_text[111:114]
		book_code = book_code.strip()
		title = title.replace('&','and')
		author = author.replace('&','and')
		course_title = course_title.replace('&','and')

		citation_output += course_code + ';' + course_title + ';' + section + ';' + professors + ';' + author + ';' + title + ';' + edition + ';' + isbn + ';' + book_code + '\n'
	else:
		continue

writer = open('cres-output.csv', 'w')
writer.write(citation_output)
writer.close()

reader3 = csv.DictReader((StringIO(citation_output)), delimiter=';', quoting=csv.QUOTE_NONE)
writer2 = open('outputxml.xml','w')

term_code_append = "-F19"
term = "AUTUMN"
status = "INACTIVE"
start_date = "2019-08-20"
end_date = "2019-12-20"
year = "2019"
creation_date = "2019-07-17"
created_by = "Rogowski, Justin"
course_index = ""
row_count = 0
output_xml = ""
#api_key = '[sandbox-api-key]'  ### sandbox
api_key = '[production-api-key]'  ###production

for row in reader3:
	#if row['course_code'] == '7503' and row['section'] == 'L10':  ##uncomment for testing on a particular course
	row_count = row_count + 1
	#if row_count == 1:  ### uncomment this line to test script on only the first citation
	#print row_count
	if row['book_code'].find('RC') == -1 and row['book_code'].find('RQ') == -1:
		continue
	else:
		new_course = row['course_code'] + "-" + row['section']
		#print new_course, row['book_code']
		if course_index.find(new_course) == -1:
			output_xml = ""	
			output_xml += "<course> \n"
			output_xml += "<code>" + row['course_code'] + term_code_append + "</code> \n"
			output_xml += "<name>" + row['course_title'] + "</name> \n"
			output_xml += "<section>" + row['section'] + "</section> \n"
			output_xml += "<academic_department></academic_department> \n"
			output_xml += "<processing_department>COURSE_UNIT</processing_department> \n"
			output_xml += "<terms><term>" + term + "</term></terms> \n"
			output_xml += "<status>INACTIVE</status> \n"
			output_xml += "<start_date>" + start_date + "</start_date> \n"
			output_xml += "<end_date>" + end_date + "</end_date> \n"
			output_xml += "<weekly_hours></weekly_hours> \n"
			output_xml += "<participants></participants> \n"
			output_xml += "<year>" + year + "</year> \n"
			output_xml += "<instructors> \n"
			prof1 = row['professor1'].split()
			prof2 = row['professor2'].split()
			prof3 = row['professor3'].split()
			prof4 = row['professor4'].split()
			output_xml += "<instructor>"
			try:
				output_xml += "<first_name>" + prof1[0] + "</first_name>"
			except:
				print "No first name for" + row['professor1']
				pass
			try:
				output_xml += "<last_name>" + prof1[1] + "</last_name>"
			except:
				print "No last name for" + row['professor1']
				pass
			output_xml += "</instructor> \n"
			if row['professor2'] != "":
				output_xml += "<instructor>"
				try:
					output_xml += "<first_name>" + prof2[0] + "</first_name>"
				except:
					print "No first name for" + row['professor2']
					pass
				try:
					output_xml += "<last_name>" + prof2[1] + "</last_name>"
				except:
					print "No last name for" + row['professor2']
					pass
				output_xml += "</instructor> \n"
			if row['professor3'] != "":
				output_xml += "<instructor>"
				try:
					output_xml += "<first_name>" + prof3[0] + "</first_name>"
				except:
					print "No first name for" + row['professor3']
					pass
				try:
					output_xml += "<last_name>" + prof3[1] + "</last_name>"
				except:
					print "No last name for" + row['professor3']
					pass
				output_xml += "</instructor> \n"
			if row['professor4'] != "":
				output_xml += "<instructor>"
				try:
					output_xml += "<first_name>" + prof4[0] + "</first_name>"
				except:
					print "No first name for" + row['professor4']
					pass
				try:
					output_xml += "<last_name>" + prof4[1] + "</last_name>"
				except:
					print "No last name for" + row['professor4']
					pass
				output_xml += "</instructor> \n"
			output_xml += "</instructors> \n"
			output_xml += "<searchable_ids> \n"
			output_xml += "<searchable_id>"
			try:
				output_xml += prof1[0]
			except:
				print "No first name for" + row['professor1']
				pass
			try:
				output_xml += " " + prof1[1]
			except:
				print "No last name for" + row['professor1']
				pass
			output_xml += "</searchable_id> \n"
			if row['professor2'] != "":
				output_xml += "<searchable_id>"
				try:
					output_xml += prof2[0]
				except:
					print "No first name for" + row['professor2']
					pass
				try:
					output_xml += " " + prof2[1]
				except:
					print "No last name for" + row['professor2']
					pass
				output_xml += "</searchable_id> \n"
			if row['professor3'] != "":
				output_xml += "<searchable_id>"
				try:
					output_xml += prof3[0]
				except:
					print "No first name for" + row['professor3']
					pass
				try:
					output_xml += " " + prof3[1]
				except:
					print "No last name for" + row['professor3']
					pass
				output_xml += "</searchable_id> \n"
			if row['professor4'] != "":
				output_xml += "<searchable_id>"
				try:
					output_xml += prof4[0]
				except:
					print "No first name for" + row['professor4']
					pass
				try:
					output_xml += " " + prof4[1]
				except:
					print "No last name for" + row['professor4']
					pass
				output_xml += "</searchable_id> \n"
			output_xml += "</searchable_ids> \n"
			output_xml += "<notes><note><content></content><creation_date>" + creation_date + "</creation_date><created_by>" + created_by + "</created_by></note></notes> \n"			
			output_xml += "</course> \n\n" 
			writer2.write(output_xml)
			course_index = course_index + new_course + ","
			new_course = ""
			
			url_course = 'https://api-na.hosted.exlibrisgroup.com/almaws/v1/courses'
			queryParams = '?' + urlencode({ quote_plus('apikey') : api_key  })
			values = output_xml
			headers = { 'Content-Type':'application/xml' }
			request_course = Request(url_course + queryParams, data=values, headers=headers)
			request_course.get_method = lambda: 'POST'
			response_body_course = urlopen(request_course).read()
			print response_body_course

			course_tree = ET.fromstring(response_body_course)
			course_id = course_tree.find('id').text
			#print course_id

			#add reading list
			output_xml = ""
			output_xml += "<reading_list> \n"
			output_xml += "<code>" + row['course_code'] + "-" + row['section'] + term_code_append + "</code> \n"
			output_xml += "<name>" + row['course_title'] + "</name> \n"
			output_xml += "<due_back_date>" + end_date + "</due_back_date> \n"
			output_xml += "<status>Complete</status> \n"
			output_xml += "<visibility>PUBLIC</visibility> \n"
			output_xml += "<publishingStatus>DRAFT</publishingStatus> \n"
			output_xml += "<notes><note><content></content><creation_date>" + creation_date + "</creation_date><created_by>" + created_by + "</created_by></note></notes> \n"
			output_xml += "</reading_list> \n\n"
			writer2.write(output_xml)

			url_readinglist = 'https://api-na.hosted.exlibrisgroup.com/almaws/v1/courses/' + course_id + '/reading-lists'
			queryParams = '?' + urlencode({ quote_plus('apikey') : api_key  })
			values = output_xml
			headers = { 'Content-Type':'application/xml' }
			request_readinglist = Request(url_readinglist + queryParams, data=values, headers=headers)
			request_readinglist.get_method = lambda: 'POST'
			response_body_readinglist = urlopen(request_readinglist).read()
			print response_body_readinglist		

			readinglist_tree = ET.fromstring(response_body_readinglist)
			readinglist_id = readinglist_tree.find('id').text
			#print readinglist_id

		#add citations
		output_xml = ""
		output_xml += "<citation> \n"
		output_xml += "<status>BeingPrepared</status> \n"
		output_xml += "<copyrights_status>NOTDETERMINED</copyrights_status> \n"
		output_xml += "<type>BK</type> \n"
		output_xml += "<secondary_type>BK</secondary_type> \n"
		output_xml += "<metadata> \n"
		output_xml += "<title>" + row['title'] + "</title> \n"
		output_xml += "<author>" + row['author'] + "</author> \n"
		output_xml += "<edition>" + row['edition'] + "</edition> \n"
		output_xml += "<isbn>" + row['isbn'] + "</isbn> \n"
		output_xml += "</metadata> \n"
		output_xml += "<defined_fields><type_attributes><attribute>BOOK</attribute><attribute_type>Requested_format</attribute_type></type_attributes></defined_fields>"
		output_xml += "</citation> \n\n"
		writer2.write(output_xml)
		print course_id, readinglist_id
		url_citation = 'https://api-na.hosted.exlibrisgroup.com/almaws/v1/courses/' + course_id + '/reading-lists/' + readinglist_id + '/citations'
		queryParams = '?' + urlencode({ quote_plus('apikey') : api_key  })
		values = output_xml
		headers = { 'Content-Type':'application/xml' }
		request_citation = Request(url_citation + queryParams, data=values, headers=headers)
		request_citation.get_method = lambda: 'POST'
		try:
			response_body_citation = urlopen(request_citation).read()
			print response_body_citation
		except HTTPError as e:
			print e.readlines()