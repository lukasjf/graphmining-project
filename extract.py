import xml.etree.ElementTree as etree


class User(object):
    def __init__(self, reputation, name, userid):
        self.reputation = reputation
        self.id = userid
        self.name = name
        self.inedges = []
        self.outedges = []

tree = etree.parse('Users.xml')
userlist = tree.getroot()

tree = etree.parse('Posts.xml')
postlist = tree.getroot()

users = {}

for child in userlist:
    attr = child.attrib
    users[attr["Id"]] = User(attr["Reputation"], attr["DisplayName"], attr["Id"])

question_mapping = {}

for q in [question for question in postlist if question.attrib["PostTypeId"] == "1"]:
    if "OwnerUserId" in q.attrib:
        question_mapping[q.attrib["Id"]] = q.attrib["OwnerUserId"]

for a in [answer for answer in postlist if answer.attrib["PostTypeId"] == "2"]:
    if "OwnerUserId" in a.attrib and a.attrib["ParentId"] in question_mapping:
        question_id = a.attrib["ParentId"]
        questioner = users[question_mapping[question_id]]
        answerer = users[a.attrib["OwnerUserId"]]
        answerer.outedges += [questioner.id]
        questioner.inedges += [answerer.id]

relevant_users = [user for user in users.values() if len(user.inedges) + len(user.outedges) > 0]

graphmlheader = """<?xml version="1.0" encoding="utf-8"?>
<graphml xmlns="http://graphml.graphdrawing.org/xmlns"
	xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
	xsi:schemaLocation="http://graphml.graphdrawing.org/xmlns
		http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd">
	<key id="d0" for="node" attr.name="DisplayName" attr.type="string">
	</key>
	<key id="d1" for="node" attr.name="Reputation" attr.type="int">
	</key>"""


with open("beer.graphml", "w") as output:
    output.write(graphmlheader)
    output.write("""<graph id="beer" edgedefault="directed">""")
    for user in relevant_users:
        output.write("""<node id="n"""+user.id+"""\">
    <data key="d0">"""+str(user.name.encode('ascii','ignore'))+"""</data>
    <data key="d1">"""+str(user.reputation)+"""</data>
</node>""")
    i = 0
    for answerer in relevant_users:
        for questioner in answerer.outedges:
            output.write("""<edge id="e"""+ str(i) + """\" source="n"""+ str(answerer.id) + """\" target="n"""+ questioner+"""\"/>""")
            i += 1
    output.write("""</graph>
</graphml>""")
    

