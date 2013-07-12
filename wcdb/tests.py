"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from minixsv import pyxsval
from genxmlif import GenXmlIfError
from models import Crisis, Person, Org, list_add, Li, Common
from loadModels import validate, populate_crisis, populate_person, populate_org
from unloadModels import clean_xml, export_crisis, export_person, export_crisis, export_organization, receive_import
import xml.etree.ElementTree as ET
from django.test.client import Client
from views import passwordValidate


#xsd = open('wcdb/WorldCrises.xsd.xml', 'r')
#psvi = pyxsval.parseAndValidate("wcdb/temp.xml", "wcdb/WorldCrises.xsd.xml",
#	xmlIfClass=pyxsval.XMLIF_ELEMENTTREE)

class ModelsCrisisTest(TestCase):

#--------------------------------------------#
#-----Unit Tests for functions from models.py
#--------------------------------------------#

	#---------------------------------------#
	#-----test_list_add

	def test_list_add(self):
	    """
	    Tests the list_add functionality of adding information to a model object's lists
	    """
	    temp   = []
	    person = "random_person"
	    list_add(temp, person)
	    self.assertEqual(temp[0], "random_person")

	#---------------------------------------#
	#-----test_li_populate

	def test_li_populate0(self):
		temp      = ET.Element('li')
		temp.set("href", "href_stuff")
		temp.text = "randomfloatingtext"
		temp_li   = Li()
		temp_li.populate(temp)
		self.assertEqual(temp_li.href, "href_stuff")
		self.assertEqual(temp_li.floating_text, "randomfloatingtext")

	def test_li_populate1(self):
		temp      = ET.Element('li')
		temp.set("href", "href_stuff")
		temp.set("embed", "embed_stuff")
		temp.set("text", "text_stuff")
		temp.text = "randomfloatingtext"
		temp_li   = Li()
		temp_li.populate(temp)
		self.assertEqual(temp_li.href, "href_stuff")
		self.assertEqual(temp_li.embed, "embed_stuff")
		self.assertEqual(temp_li.text, "text_stuff")
		self.assertEqual(temp_li.floating_text, "randomfloatingtext")

	def test_li_populate2(self):
		temp      = ET.Element('li')
		temp.text = "randomfloatingtext"
		temp_li   = Li()
		temp_li.populate(temp)
		self.assertEqual(temp_li.floating_text, "randomfloatingtext")

	#---------------------------------------#
	#-----test_clean_li_xml
	
	def test_clean_li_xml0(self):
		dirt = "happy&go&lucky&&&go&happy"
		temp      = ET.Element('li')
		temp.set("href", dirt)
		temp.set("embed", dirt)
		temp.set("text", dirt)
		temp.text = dirt
		temp_li   = Li()
		temp_li.populate(temp)
		href_clean = temp_li.clean_li_xml(temp_li.href)
		embed_clean = temp_li.clean_li_xml(temp_li.embed)
		text_clean = temp_li.clean_li_xml(temp_li.text)
		floating_text_clean = temp_li.clean_li_xml(temp_li.floating_text)
		standard_clean = "happy&amp;go&amp;lucky&amp;&amp;&amp;go&amp;happy"

		self.assertEqual(href_clean, standard_clean)
		self.assertEqual(embed_clean, standard_clean)
		self.assertEqual(text_clean, standard_clean)
		self.assertEqual(floating_text_clean, standard_clean)

	#---------------------------------------#
	#-----test_li_print_xml
	
	def test_li_print_xml0(self):
		temp      = ET.Element('li')
		temp.set("href", "href_stuff")
		temp.set("embed", "embed_stuff")
		temp.set("text", "text_stuff")
		temp.text = "randomfloatingtext"
		temp_li   = Li()
		temp_li.populate(temp)
		temp_string = temp_li.print_xml()
		correct_string = "<li> href=\"href_stuff\"</li><li> embed=\"embed_stuff\"</li><li>text_stuff</li><li>randomfloatingtext</li>"
		#print temp_string
		#print correct_string
		self.assertEqual(temp_string, correct_string)

	#---------------------------------------#
	#-----test_common_populate

	def test_common_populate0(self):
		temp_com = Common()
		xml_string = '<Common><Citations><li>The Hindustan Times</li></Citations><ExternalLinks><li href="http://en.wikipedia.org/wiki/2013_North_India_floods">Wikipedia</li></ExternalLinks><Images><li embed="http://timesofindia.indiatimes.com/photo/15357310.cms" /></Images><Videos><li embed="//www.youtube.com/embed/qV3s7Sa6B6w" /></Videos><Maps><li embed="https://www.google.com/maps?sll=30.08236989592049,79.31189246107706&amp;sspn=3.2522150867582833,7.2072687770004205&amp;t=m&amp;q=uttarakhand&amp;dg=opt&amp;ie=UTF8&amp;hq=&amp;hnear=Uttarakhand,+India&amp;ll=30.066753,79.0193&amp;spn=2.77128,5.07019&amp;z=8&amp;output=embed" /></Maps><Feeds><li embed="[WHATEVER A FEED URL LOOKS LIKE]" /></Feeds><Summary>Lorem ipsum...</Summary></Common>'
		root = ET.fromstring(xml_string)
		temp_com.populate(root)

		self.assertEqual(temp_com.citations[0].floating_text, "The Hindustan Times")
		self.assertEqual(temp_com.external_links[0].href, "http://en.wikipedia.org/wiki/2013_North_India_floods")
		self.assertEqual(temp_com.images[0].embed, "http://timesofindia.indiatimes.com/photo/15357310.cms")
		self.assertEqual(temp_com.videos[0].embed, "//www.youtube.com/embed/qV3s7Sa6B6w")
		#self.assertEqual(temp_com.maps[0].href, "https://www.google.com/maps?sll=30.08236989592049,79.31189246107706&amp;sspn=3.2522150867582833,7.2072687770004205&amp;t=m&amp;q=uttarakhand&amp;dg=opt&amp;ie=UTF8&amp;hq=&amp;hnear=Uttarakhand,+India&amp;ll=30.066753,79.0193&amp;spn=2.77128,5.07019&amp;z=8&amp;output=embed")
		self.assertEqual(temp_com.feeds[0].embed, "[WHATEVER A FEED URL LOOKS LIKE]")
		self.assertEqual(temp_com.videos[0].embed, "//www.youtube.com/embed/qV3s7Sa6B6w")

	def test_common_populate1(self):
		temp_com = Common()
		xml_string = '<Common><Citations><li>Random Citation</li></Citations><ExternalLinks><li href="http://en.wikipedia.org/wiki/2013_North_India_floods">Wikipedia</li></ExternalLinks><Images><li embed="http://timesofindia.indiatimes.com/photo/15357310.cms" /></Images><Summary>Random Summary</Summary></Common>'
		root = ET.fromstring(xml_string)
		temp_com.populate(root)

		self.assertEqual(temp_com.citations[0].floating_text, "Random Citation")
		self.assertEqual(temp_com.external_links[0].href, "http://en.wikipedia.org/wiki/2013_North_India_floods")
		self.assertEqual(temp_com.images[0].embed, "http://timesofindia.indiatimes.com/photo/15357310.cms")
		#self.assertEqual(temp_com.videos[0], "Random Summary")
	
	def test_common_populate2(self):
		temp_com = Common()
		xml_string = "<Common><Citations><li>Random Citation</li></Citations><Summary>Random Summary</Summary></Common>"
		root = ET.fromstring(xml_string)
		temp_com.populate(root)

		self.assertEqual(temp_com.citations[0].floating_text, "Random Citation")

	#---------------------------------------#
	#-----test_xml_from_li

	def test_xml_from_li0(self):
		temp_com = Common()
		xml_string = "<Common><Citations><li>RandomCitation</li></Citations><ExternalLinks><li>RandomLink</li></ExternalLinks><Images><li>RandomImage</li></Images><Videos><li>RandomVideo</li></Videos></Common>"
		root = ET.fromstring(xml_string)
		temp_com.populate(root)
		li_xml = "<Common>"
		c_cites = temp_com.xml_from_li("Citations", temp_com.citations)
		li_xml += c_cites
		c_links = temp_com.xml_from_li("ExternalLinks", temp_com.external_links)
		li_xml += c_links
		c_ims = temp_com.xml_from_li("Images", temp_com.images)
		li_xml += c_ims
		c_vids = temp_com.xml_from_li("Videos", temp_com.videos)
		li_xml += c_vids
		li_xml += "</Common>"
		self.assertEqual(li_xml, xml_string )

	#---------------------------------------#
	#-----test_print_xml
	
	def test_print_xml0(self):
		temp_com = Common()
		xml_string = "<Common><Citations><li>RandomCitation</li></Citations><ExternalLinks><li>RandomLink</li></ExternalLinks><Images><li>RandomImage</li></Images><Videos><li>RandomVideo</li></Videos><Summary>Random Summary</Summary></Common>"
		root = ET.fromstring(xml_string)
		temp_com.populate(root)
		common_xml = temp_com.print_xml()

		#print "xml_string : ", xml_string, len(xml_string)
		#print "common_xml : ", common_xml, len(common_xml)

		self.assertEqual(xml_string, common_xml)



class unloadModelsCrisisTest(TestCase):

#---------------------------------------------------#
#-----Unit Tests for functions from unloadModels.py
#---------------------------------------------------#

	#---------------------------------------#
	#-----test_clean_xml (paranoid clean for things that are not li objects)
	
	def test_clean_xml0(self):
		dirt = "happy&go&lucky&&&go&happy"
		dirt_to_clean = clean_xml(dirt)
		standard_clean = "happy&amp;go&amp;lucky&amp;&amp;&amp;go&amp;happy"
		self.assertEqual(dirt_to_clean, standard_clean)
	
	#---------------------------------------#
	#-----test_export_crisis

	def test_export_crisis(self):
		xml_string = "<WC><Crisis ID=\"CRI_UEGYPT\" Name=\"Political unrest in Egypt\"><People><Person ID=\"PER_HMUBAR\" /><Person ID=\"PER_RLAKAH\" /><Person ID=\"PER_ELBARA\" /><Person ID=\"PER_MMORSI\" /></People><Organizations><Org ID=\"ORG_MUSBRO\" /><Org ID=\"ORG_EGYGOV\" /></Organizations><Kind>Revolution</Kind><Date>2011-01-25</Date><Time>09:00:00+05:30</Time><Locations><li>Cairo</li><li>Alexandria</li><li>Mansoura</li><li>Suez</li></Locations><HumanImpact><li>Anger towards the corruption in the Egyption political system influenced millions of protesters to join plaza marches and other demonstrations against the government.</li><li>Many protests were organized using social media, demonstrating the powerful new influence of technology over politics and human action.</li><li>The movement united Egytian citizens over a spectrum of socio-economic and religious foundations.</li><li>Eight hundred forty-six people were killed and around six thousand have assumed injuries participating in demonstrations against Egypt's police and military.</li></HumanImpact><EconomicImpact><li>As the government is restructured in Egypt, the economic situation of people will change based our their dependency on the corrupt system as a source of wealth.</li><li>It is possible that the gap in leadership will be taken advantage of and a party with a different form of corruption will refactor the system completely.</li><li>If Egypt adopts a better set of leaders, it may positively influence its trade with Western countries.</li><li> Importers of Egypt's oil will see prices of gasoline affected by the turnover of Egypt's political leaders.</li></EconomicImpact><ResourcesNeeded><li>Money</li><li>Support for positive political reorganization</li><li>New leaders (non-corrupt)</li></ResourcesNeeded><WaysToHelp><li> href=\"http://en.wikipedia.org/wiki/Egyptian_Organization_for_Human_Rights\"</li><li> Egyption Organization for Human Rights</li><li> href=\"http://www.americanprogress.org/\"</li><li> Center for American Progress</li><li> href=\"http://www.cewla.org/\"</li><li> Center for Egyptian Women's Legal Assistance (CEWLA)</li></WaysToHelp><Common><Citations><li> href=\"http://www.bloomberg.com/news/2013-07-05/gasoline-rises-on-u-s-job-gains-amid-political-unrest-in-egypt.html\"</li><li> Powell, Barbara. Gasoline Rises on US Job Gains Amid Political Unrest in Egypt. 2013 Jul 5. Bloomberg.</li><li> href=\"http://www.economist.com/topics/egyptian-politics\"</li><li> The Economist. Egyptian politics.</li></Citations><ExternalLinks><li> href=\"http://www.livescience.com/38023-protecting-egypt-artifacts-during-crisis.html\"</li><li> Egypt's National Treasures Threatened by Political Unrest</li><li> href=\"https://en.wikipedia.org/wiki/2011_Egyptian_revolution\"</li><li> Wikipedia : Egyptian Revolution of 2011</li><li> href=\"http://www.bbc.co.uk/news/world-middle-east-23228297\"</li><li> Egypt's political unrest causes regional concern</li></ExternalLinks><Images><li> embed=\"http://radio.foxnews.com/wp-content/uploads/2011/02/egypt-drama-2.jpg\"</li><li> Egypt unrest continues</li><li> embed=\"http://media.themalaysianinsider.com/images/uploads/2011/january/31/mubarak.jpg\"</li><li> Down with Mubarak Protest sign</li></Images><Videos><li> embed=\"https://www.youtube.com/watch?v=ze1hcPejorQ\"</li><li> Egypt's president ousted in military coup\" </li><li> embed=\"https://www.youtube.com/watch?v=1dGDv7kzJEI\"</li><li> Obama, staff huddle over Egypt</li><li> embed=\"https://www.youtube.com/watch?v=bptZAPw2lgQ\"</li><li> Analysis: Victory or 'a sad day' for Egypt?</li><li> embed=\"https://www.youtube.com/watch?v=GcLmi0ZdEpc\"</li><li> Protest in Egypt - Jan 25, 2011</li></Videos><Summary>Egypt is on the brink of drastic political changes that will affect its future political systems and socioeconic climate.</Summary></Common></Crisis></WC>"
		crisis_list1 = []
		root1 = ET.fromstring(xml_string)
		populate_crisis(root1, crisis_list1)
		#print len(crisis_list1[0].people)
		#for person in crisis_list1[0].people :
		#	print person
		# crisis_xml = export_crisis(crisis_list1[0])
		# check_string = xml_string [4:-5]

		# self.assertEqual(check_string, crisis_xml)


	#---------------------------------------#
	#-----test_export_person

	def test_export_person(self):
		person_string = "<WC><Person ID=\"PER_HMUBAR\" Name=\"Hosni Mubarak\"><Crises><Crisis ID=\"CRI_UEGYPT\" /></Crises><Organizations><Org ID=\"ORG_MUSBRO\" /><Org ID=\"ORG_EGYGOV\" /></Organizations><Kind>Politician</Kind><Location>Egypt</Location><Common></Common></Person></WC>"
		person_list = []
		root = ET.fromstring(person_string)
		populate_person(root, person_list)
		person_xml = export_person(person_list[0])
		check_string = person_string [4:-5]

		self.assertEqual(check_string, person_xml)

	#---------------------------------------#
	#-----test_export_organization

	def test_export_org(self):
		org_string = "<WC><Organization ID=\"ORG_MUSBRO\" Name=\"The Muslim Brotherhood\"><Crises><Crisis ID=\"CRI_UEGYPT\" /></Crises><People><Person ID=\"PER_ELBARA\" /><Person ID=\"PER_HMUBAR\" /><Person ID=\"PER_RLAKAH\" /><Person ID=\"PER_MMORSI\" /></People><Kind>Islamic Movement</Kind><Location>Egypt</Location><Common></Common></Organization></WC>"
		org_list = []
		root8 = ET.fromstring(org_string)
		populate_org(root8, org_list)
		org_xml = export_organization(org_list[0])
		check_string = org_string [4:-5]

		self.assertEqual(check_string, org_xml)


	#---------------------------------------#
	#-----test_receive_import


class loadModelsCrisisTest(TestCase):

#------------------------------------------------#
#-----Unit Tests for functions from loadModels.py
#------------------------------------------------#

	#---------------------------------------#
	#-----test_validate

	def test_validate0(self):
		f = open('wcdb/xml0.xml')
		self.assertEqual(type(f), file)
		self.assert_(validate(f) != False)

	def test_validate1(self):
		f = open('wcdb/xml1.xml')
		self.assertEqual(type(f), file)
		self.assert_(type(validate(f)) == str)

	def test_validate2(self):
		f = open('wcdb/xml2.xm')
		self.assertEqual(type(f), file)
		self.assertEqual(validate(f), False)

	#---------------------------------------#
	#-----test_populate_models

	#---------------------------------------#
	#-----test_populate_crisis

	def test_populate_crisis(self):
		xml_string = "<WC><Crisis ID=\"CRI_UEGYPT\" Name=\"Political unrest in Egypt\"><People><Person ID=\"PER_HMUBAR\" /><Person ID=\"PER_RLAKAH\" /><Person ID=\"PER_ELBARA\" /><Person ID=\"PER_MMORSI\" /></People><Organizations><Org ID=\"ORG_MUSBRO\" /><Org ID=\"ORG_EGYGOV\" /></Organizations><Kind>Revolution</Kind><Date>2011-01-25</Date><Time>09:00:00+05:30</Time><Locations><li>Cairo</li><li>Alexandria</li><li>Mansoura</li><li>Suez</li></Locations><HumanImpact><li>Anger towards the corruption in the Egyption political system influenced millions of protesters to join plaza marches and other demonstrations against the government.</li><li>Many protests were organized using social media, demonstrating the powerful new influence of technology over politics and human action.</li><li>The movement united Egytian citizens over a spectrum of socio-economic and religious foundations.</li><li>Eight hundred forty-six people were killed and around six thousand have assumed injuries participating in demonstrations against Egypt's police and military.</li></HumanImpact><EconomicImpact><li>As the government is restructured in Egypt, the economic situation of people will change based our their dependency on the corrupt system as a source of wealth.</li><li>It is possible that the gap in leadership will be taken advantage of and a party with a different form of corruption will refactor the system completely.</li><li>If Egypt adopts a better set of leaders, it may positively influence its trade with Western countries.</li><li> Importers of Egypt's oil will see prices of gasoline affected by the turnover of Egypt's political leaders.</li></EconomicImpact><ResourcesNeeded><li>Money</li><li>Support for positive political reorganization</li><li>New leaders (non-corrupt)</li></ResourcesNeeded><WaysToHelp><li> href=\"http://en.wikipedia.org/wiki/Egyptian_Organization_for_Human_Rights\"</li><li> Egyption Organization for Human Rights</li><li> href=\"http://www.americanprogress.org/\"</li><li> Center for American Progress</li><li> href=\"http://www.cewla.org/\"</li><li> Center for Egyptian Women's Legal Assistance (CEWLA)</li></WaysToHelp><Common><Citations><li> href=\"http://www.bloomberg.com/news/2013-07-05/gasoline-rises-on-u-s-job-gains-amid-political-unrest-in-egypt.html\"</li><li> Powell, Barbara. Gasoline Rises on US Job Gains Amid Political Unrest in Egypt. 2013 Jul 5. Bloomberg.</li><li> href=\"http://www.economist.com/topics/egyptian-politics\"</li><li> The Economist. Egyptian politics.</li></Citations><ExternalLinks><li> href=\"http://www.livescience.com/38023-protecting-egypt-artifacts-during-crisis.html\"</li><li> Egypt's National Treasures Threatened by Political Unrest</li><li> href=\"https://en.wikipedia.org/wiki/2011_Egyptian_revolution\"</li><li> Wikipedia : Egyptian Revolution of 2011</li><li> href=\"http://www.bbc.co.uk/news/world-middle-east-23228297\"</li><li> Egypt's political unrest causes regional concern</li></ExternalLinks><Images><li> embed=\"http://radio.foxnews.com/wp-content/uploads/2011/02/egypt-drama-2.jpg\"</li><li> Egypt unrest continues</li><li> embed=\"http://media.themalaysianinsider.com/images/uploads/2011/january/31/mubarak.jpg\"</li><li> Down with Mubarak Protest sign</li></Images><Videos><li> embed=\"https://www.youtube.com/watch?v=ze1hcPejorQ\"</li><li> Egypt's president ousted in military coup\" </li><li> embed=\"https://www.youtube.com/watch?v=1dGDv7kzJEI\"</li><li> Obama, staff huddle over Egypt</li><li> embed=\"https://www.youtube.com/watch?v=bptZAPw2lgQ\"</li><li> Analysis: Victory or 'a sad day' for Egypt?</li><li> embed=\"https://www.youtube.com/watch?v=GcLmi0ZdEpc\"</li><li> Protest in Egypt - Jan 25, 2011</li></Videos><Summary>Egypt is on the brink of drastic political changes that will affect its future political systems and socioeconic climate.</Summary></Common></Crisis></WC>"
		crisis_list = []
		root = ET.fromstring(xml_string)
		populate_crisis(root, crisis_list)


	#---------------------------------------#
	#-----test_populate_person

	#---------------------------------------#
	#-----test_populate_org


class viewsTest(TestCase):

#--------------------------------------------#
#-----Unit Tests for functions from views.py
#--------------------------------------------#

	#---------------------------------------#
	#-----test_crisisView
	#---------------------------------------#

	# tests that user can see our pages 
	def test_indexView(self):
		response = self.client.get("http://localhost:8000/")
		self.assertEqual(response.status_code, 200)

	def test_crisisView0(self):
		response = self.client.get("http://localhost:8000/crisis/1")
		self.assertEqual(response.status_code, 200)

	def test_crisisView1(self):
		response = self.client.get("http://localhost:8000/crisis/2")
		self.assertEqual(response.status_code, 200)

	def test_crisisView2(self):
		response = self.client.get("http://localhost:8000/crisis/3")
		self.assertEqual(response.status_code, 200)

	def test_orgsView0(self):
		response = self.client.get("http://localhost:8000/orgs/1")
		self.assertEqual(response.status_code, 200)

	def test_orgsView1(self):
		response = self.client.get("http://localhost:8000/orgs/2")
		self.assertEqual(response.status_code, 200)

	def test_orgsView2(self):
		response = self.client.get("http://localhost:8000/orgs/3")
		self.assertEqual(response.status_code, 200)

	def test_peopleView0(self):
		response = self.client.get("http://localhost:8000/people/1")
		self.assertEqual(response.status_code, 200)

	def test_peopleView1(self):
		response = self.client.get("http://localhost:8000/people/2")
		self.assertEqual(response.status_code, 200)

	def test_peopleView2(self):
		response = self.client.get("http://localhost:8000/people/3")
		self.assertEqual(response.status_code, 200)

	"""
	Creates an infinite loop!
	def test_unittestView(self):
		response = self.client.get("http://localhost:8000/unittests/")
		self.assertEqual(response.status_code, 200)
	"""

	def test_importView1(self):
		response = self.client.get("http://localhost:8000/import/")
		self.assertEqual(response.status_code, 200)

	def test_importView2(self):
		c = Client()
		with open('wcdb/xml0.xml') as upload:
			response = self.client.post("http://localhost:8000/import/", {'password': "ateam", 'xmlvalue': upload}, follow = True)
        	self.assertEqual(response.status_code, 200) # Redirect on form success

	def test_passwordValidate0(self):
		pw = "ateam"
		result = passwordValidate(pw)
		self.assert_(result)

	def test_passwordValidate1(self):
		pw = "someotherteam"
		result = passwordValidate(pw)
		self.assert_(not (result))

	def test_exportView(self):
		response = self.client.get("http://127.0.0.1:8000/export/")
		self.assertEqual(response.status_code, 200)