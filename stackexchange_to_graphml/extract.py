import sys
import xml.etree.ElementTree as etree


class User(object):
    def __init__(self, reputation, name, userid):
        self.reputation = reputation
        self.id = userid
        self.name = name
        self.inedges = set()
        self.outedges = set()

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

#answer edges
if 'a' in sys.argv:
    for a in [answer for answer in postlist if answer.attrib["PostTypeId"] == "2"]:
        if "OwnerUserId" in a.attrib and a.attrib["ParentId"] in post_mapping:
            question_id = a.attrib["ParentId"]
            questioner = users[post_mapping[question_id]]
            answerer = users[a.attrib["OwnerUserId"]]
            if answerer != questioner:
                answerer.outedges.add(questioner.id)
                questioner.inedges.add(answerer.id)
	
#comment edges	
if 'c' in sys.argv:
    for c in commentlist:
        if "UserId" in c.attrib and c.attrib["PostId"] in post_mapping:
            post_id = c.attrib["PostId"]
            poster = users[post_mapping[post_id]]
            commenter = users[c.attrib["UserId"]]
            if commenter != poster:
                commenter.outedges.add(poster.id)
                poster.inedges.add(commenter.id)

#shared answers edges
answers_mapping = {}

if 's' in sys.argv:
    for a in [answer for answer in postlist if answer.attrib["PostTypeId"] == "2"]:
        if "OwnerUserId" in a.attrib and a.attrib["ParentId"] in post_mapping:
            question_id = a.attrib["ParentId"]
            answerer_id = a.attrib["OwnerUserId"]
            answerer = users[answerer_id]
            if not question_id in answers_mapping:
                answers_mapping[question_id] = []
            for shared_answerer_id in answers_mapping[question_id]:
                shared_answerer = users[shared_answerer_id]
                if shared_answerer != answerer:
                    answerer.outedges.add(shared_answerer_id)
                    answerer.inedges.add(shared_answerer_id)
                    shared_answerer.outedges.add(answerer_id)
                    shared_answerer.inedges.add(answerer_id)
            answers_mapping[question_id] += [answerer_id]
		
relevant_users = [user for user in users.values() if len(user.outedges) > 0]

graphmlheader = """<?xml version="1.0" encoding="utf-8"?>
<graphml xmlns="http://graphml.graphdrawing.org/xmlns"
	xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
	xsi:schemaLocation="http://graphml.graphdrawing.org/xmlns
		http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd">
	<key id="d0" for="node" attr.name="DisplayName" attr.type="string"></key>
	<key id="d1" for="node" attr.name="Reputation" attr.type="int"></key>"""


with open("beer.graphml", "w") as output:
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
    for source in relevant_users:
        for target in source.outedges:
            output.write("""
		<edge id="e"""+ str(i) + """\" source="n"""+ str(source.id) + """\" target="n"""+ target+"""\"/>""")
            i += 1
    output.write("""
	</graph>
</graphml>""")

print('nodes: ' + str(len(relevant_users)))
print('edges: ' + str(i))
    

