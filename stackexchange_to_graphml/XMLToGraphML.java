import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.nio.charset.Charset;
import java.util.HashMap;
import java.util.Map;

import javax.xml.stream.XMLInputFactory;
import javax.xml.stream.XMLStreamException;
import javax.xml.stream.XMLStreamReader;


public class XMLToGraphML {

	public static void main(String[] args){
		if(args.length < 3){
			System.out.println("4 parameters: xmlUserFile, xmlPostFile, graphName, graphmlFile");
			return;
		}
		String xmlUserFile = args[0];
		String xmlPostFile = args[1];
		String graphmlFile = args[2];
		String graphName = args[3];
		
		try {
			OutputStreamWriter bw = new OutputStreamWriter(new FileOutputStream(graphmlFile), Charset.forName("UTF-8"));
			
			
	        XMLInputFactory xmlInFact = XMLInputFactory.newInstance();
	        XMLStreamReader userReader = xmlInFact.createXMLStreamReader(new FileInputStream(xmlUserFile));
	        XMLStreamReader postReader = xmlInFact.createXMLStreamReader(new FileInputStream(xmlPostFile));
	        
			Map<String, String> userIdToNodeId = writeNodes(userReader, bw, graphName);
			writeEdges(postReader, bw, userIdToNodeId);

            writeEndDocument(bw);
			bw.flush();
			bw.close();
	        userReader.close();
	        postReader.close();
		} catch (IOException | XMLStreamException e) {
			e.printStackTrace();
		}
	}
	
	private static void writeEdges(XMLStreamReader reader, OutputStreamWriter bw, Map<String, String> userIdToNodeId) throws XMLStreamException, IOException {
		long id = 0;
		Map<String, String> questionOwnerNodeIds = new HashMap<>();
		while(reader.hasNext()) {
            switch(reader.getEventType()){
            case XMLStreamReader.START_ELEMENT:
            	if(reader.getLocalName().equals("row")){
            		int type = Integer.parseInt(reader.getAttributeValue(null, "PostTypeId"));
            		if(type == 1){
            			String ownerUserId = reader.getAttributeValue(null, "OwnerUserId");
            			if(ownerUserId == null){
            				reader.next();
            				continue;
            			}
            			String ownerNodeId = userIdToNodeId.get(ownerUserId);
            			String questionId = reader.getAttributeValue(null, "Id");
            			questionOwnerNodeIds.put(questionId, ownerNodeId);
            		}
            		else if(type == 2){
            			String ownerUserId = reader.getAttributeValue(null, "OwnerUserId");
            			if(ownerUserId == null){
            				reader.next();
            				continue;
            			}
            			String ownerNodeId = userIdToNodeId.get(ownerUserId);
            			String parentId = reader.getAttributeValue(null, "ParentId");
            			String parentOwnerNodeId = questionOwnerNodeIds.get(parentId);
            			if(parentOwnerNodeId == null){
            				reader.next();
            				continue;
            			}
            			writeEdge(bw, id, ownerNodeId, parentOwnerNodeId);
                		id++;
            		}
            	}
            	break;
            }
            reader.next();
        }
	}

	private static void writeEdge(OutputStreamWriter bw, long id, String sourceId, String targetId) throws IOException {
		bw.write("\t\t\t<edge id=\"");
		bw.write("e" + id + "\"");
		bw.write(" source=\"" + sourceId + "\" ");
		bw.write(" target=\"" + targetId + "\"/>\n");
	}

	private static Map<String, String> writeNodes(XMLStreamReader reader, OutputStreamWriter bw, String graphName) throws XMLStreamException, IOException {
		long id = 0;
		Map<String, String> userIdToNodeId = new HashMap<>();
        while(reader.hasNext()) {
            switch(reader.getEventType()){
            case XMLStreamReader.START_DOCUMENT:
            	writeStartDocument(reader, bw, graphName);
            	break;
            case XMLStreamReader.START_ELEMENT:
            	if(reader.getLocalName().equals("row")){
            		String userId = reader.getAttributeValue(null, "Id");
            		String nodeId = writeNodeStartElement(reader, bw, id);
            		userIdToNodeId.put(userId, nodeId);
            		id++;
            	}
            	break;
            case XMLStreamReader.END_ELEMENT:
            	if(reader.getLocalName().equals("row")){
            		writeNodeEndElement(reader, bw);
            	}
            	break;
            }
            reader.next();
        }
        return userIdToNodeId;
	}

	private static void writeNodeEndElement(XMLStreamReader reader, OutputStreamWriter bw) throws IOException {
		bw.write("\t\t</node>\n");
	}

	private static String writeNodeStartElement(XMLStreamReader reader, OutputStreamWriter bw, long id) throws IOException{
		String nodeId = "n" + id;
		bw.write("\t\t<node id=\"");
		bw.write(nodeId);
		bw.write("\">\n");
		bw.write("\t\t\t<data key=\"d0\">"+ reader.getAttributeValue(null, "DisplayName") +"</data>\n");
		bw.write("\t\t\t<data key=\"d1\">"+ reader.getAttributeValue(null, "Reputation") +"</data>\n");
		return nodeId;
	}

	private static void writeGraphStartElement(XMLStreamReader reader, OutputStreamWriter bw, String graphName) throws IOException {
		bw.write("\t<graph id=\"" + graphName + "\" edgedefault=\"directed\">\n");
	}
	
	private static void writeGraphEndElement(OutputStreamWriter bw) throws IOException {
		bw.write("\t</graph>\n");
	}
	
	private static void writeStartDocument(XMLStreamReader reader, OutputStreamWriter bw, String graphName) throws IOException {
		bw.write("<?xml version=\"");
		bw.write(reader.getVersion());
		bw.write("\" encoding=\"");
		bw.write(reader.getEncoding());
		bw.write("\"?>");
		bw.write("\n");
		bw.write(	"<graphml xmlns=\"http://graphml.graphdrawing.org/xmlns\"\n" + 
					"\txmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n" +
					"\txsi:schemaLocation=\"http://graphml.graphdrawing.org/xmlns\n" +
					"\t\thttp://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd\">\n");
		bw.write("\t<key id=\"d0\" for=\"node\" attr.name=\"DisplayName\" attr.type=\"string\">\n");
		bw.write("\t</key>\n");
		bw.write("\t<key id=\"d1\" for=\"node\" attr.name=\"Reputation\" attr.type=\"int\">\n");
		bw.write("\t</key>\n");
		writeGraphStartElement(reader, bw, graphName);
	}

	private static void writeEndDocument(OutputStreamWriter bw) throws IOException {
		writeGraphEndElement(bw);
		bw.write("</graphml>");
	}
	
}
