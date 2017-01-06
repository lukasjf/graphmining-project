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

tree = etree.parse('Comments.xml')
commentlist = tree.getroot()

users = {}

for child in userlist:
    attr = child.attrib
    users[attr["Id"]] = User(attr["Reputation"], attr["DisplayName"], attr["Id"])

post_mapping = {}

for p in postlist:
    if "OwnerUserId" in p.attrib:
        post_mapping[p.attrib["Id"]] = p.attrib["OwnerUserId"]
		
for c in commentlist:
	if "UserId" in c.attrib and c.attrib["PostId"] in post_mapping:
		post_id = c.attrib["PostId"]
		poster = users[post_mapping[post_id]]
		commenter = users[c.attrib["UserId"]]
		commenter.outedges += [poster.id]
		poster.inedges += [commenter.id]
	
relevant_users = [user for user in users.values() if len(user.inedges) + len(user.outedges) > 0]

graphmlheader = """<?xml version="1.0" encoding="utf-8"?>
<graphml xmlns="http://graphml.graphdrawing.org/xmlns"
	xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
	xsi:schemaLocation="http://graphml.graphdrawing.org/xmlns
		http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd">
	<key id="d0" for="node" attr.name="DisplayName" attr.type="string"></key>
	<key id="d1" for="node" attr.name="Reputation" attr.type="int"></key>"""


with open("beer_comments.graphml", "w") as output:
    output.write(graphmlheader)
    output.write("""
	<graph id="beer" edgedefault="directed">""")
    for user in relevant_users:
        output.write("""
		<node id="n"""+user.id+"""\">
			<data key="d0">"""+str(user.name.encode('ascii','ignore'))+"""</data>
			<data key="d1">"""+str(user.reputation)+"""</data>
		</node>""")
    i = 0
    for answerer in relevant_users:
        for questioner in answerer.outedges:
            output.write("""
		<edge id="e"""+ str(i) + """\" source="n"""+ str(answerer.id) + """\" target="n"""+ questioner+"""\"/>""")
            i += 1
    output.write("""
	</graph>
</graphml>""")
    

